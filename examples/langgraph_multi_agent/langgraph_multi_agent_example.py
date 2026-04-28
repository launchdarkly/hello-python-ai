import os
from dotenv import load_dotenv
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient
from ldai.tracker import TokenUsage
from ldai_langchain import get_ai_metrics_from_response
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from langgraph.types import Command
from typing_extensions import TypedDict

load_dotenv()

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config keys for the two agents
analyzer_config_key = os.getenv('LAUNCHDARKLY_ANALYZER_CONFIG_KEY', 'code-review-analyzer')
documentation_config_key = os.getenv('LAUNCHDARKLY_DOCUMENTATION_CONFIG_KEY', 'code-review-documentation')

# Custom state class for the code review workflow
class CodeReviewState(TypedDict):
    messages: list
    analysis: str
    documentation: str
    final_report: str

def map_provider_to_langchain(provider_name):
    """Map LaunchDarkly provider names to LangChain provider names."""
    provider_mapping = {
        'gemini': 'google_genai'
    }
    lower_provider = provider_name.lower()
    return provider_mapping.get(lower_provider, lower_provider)

def track_langgraph_metrics(tracker, func, prev_message_count=0):
    """
    Track LangGraph agent operations with LaunchDarkly metrics.
    """
    try:
        result = tracker.track_duration_of(func)
        tracker.track_success()

        total_input_tokens = 0
        total_output_tokens = 0
        total_tokens = 0
        if "messages" in result:
            new_messages = result["messages"][prev_message_count:]
            for message in new_messages:
                metrics = get_ai_metrics_from_response(message)
                if metrics.usage:
                    total_input_tokens += metrics.usage.input
                    total_output_tokens += metrics.usage.output
                    total_tokens += metrics.usage.total
        if total_tokens > 0:
            tracker.track_tokens(
                TokenUsage(
                    input=total_input_tokens,
                    output=total_output_tokens,
                    total=total_tokens,
                )
            )
    except Exception:
        tracker.track_error()
        raise
    return result

# Note: Agent instructions are now configured through LaunchDarkly AI flags
# The SDK will use the instructions from the flag configuration

def create_agent_with_config(aiclient, config_key, context):
    """Create a LangChain model with LaunchDarkly AI config."""
    # Pass a default for improved resiliency when the agent config is unavailable
    # or LaunchDarkly is unreachable; omit for a disabled default.
    # Example (enabled default):
    #   default = AIAgentConfigDefault(
    #       enabled=True,
    #       instructions='You are a helpful assistant.',
    #   )
    #   agent_config = aiclient.agent_config(config_key, context, default=default)
    agent_config = aiclient.agent_config(config_key, context)

    if not agent_config.enabled:
        return None, None, True
    
    langchain_provider = map_provider_to_langchain(agent_config.provider.name)
    llm = init_chat_model(
        model=agent_config.model.name,
        model_provider=langchain_provider,
    )
    
    # Create a React agent with the LLM
    agent = create_react_agent(llm, [], prompt=agent_config.instructions)
    
    return agent, agent_config.tracker, False

def ai_node(
    state: CodeReviewState, 
    aiclient, 
    context, 
    config_key: str, 
    state_key: str,
    next_step: str
) -> Command:
    """Unified function to process code with AI agents (analysis or documentation)."""
    print(f"Starting node for {config_key}")
    
    try:
        agent, tracker, disabled = create_agent_with_config(
            aiclient, config_key, context
        )
        
        if disabled:
            return Command(
                goto=END,
                update={
                    "messages": state["messages"],
                    state_key: f"AI Config {config_key} is disabled. Node for {config_key} skipped."
                }
            )
        
        # Track and execute the AI operation
        prev_message_count = len(state["messages"])
        completion = track_langgraph_metrics(tracker, lambda: agent.invoke({"messages": state["messages"]}), prev_message_count)

        # Extract the content from the agent's response
        content = ""
        if completion["messages"]:
            last_message = completion["messages"][-1]
            if hasattr(last_message, 'content'):
                content = last_message.content
        
        # Return Command to update state and route to next step
        return Command(
            goto=next_step,
            update={
                "messages": completion["messages"],
                state_key: content
            }
        )
        
    except Exception as e:
        print(f"❌ Error in node for {config_key}: {e}")
        return Command(
            goto=END,
            update={
                "messages": [{"role": "system", "content": f"Error: {str(e)}"}],
                state_key: f"Error: {str(e)}"
            }
        )

def create_final_report(state: CodeReviewState) -> Command:
    """Combine analysis and documentation into a final report."""
    print("Creating final report")
    
    # Use the stored analysis and documentation from state
    analysis = state.get("analysis", "No analysis available")
    documentation = state.get("documentation", "No documentation available")
    
    final_report = f"""# Code Review Report

## Code Analysis
{analysis}

## Generated Documentation
{documentation}

---
*This report was generated by the LaunchDarkly Code Review Duo using LangGraph*"""
    
    print("✅ Final report created")
    
    return Command(
        goto=END,
        update={
            "final_report": final_report
        }
    )

def main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    aiclient = LDAIClient(ldclient.get())
    print("*** SDK successfully initialized")

    # Set up the evaluation context
    context = (
        Context
        .builder('code-review-user')
        .kind('user')
        .name('Code Reviewer')
        .build()
    )

    # Sample code for review
    sample_code = '''
def process_user_data(user_input):
    """Process user input and return processed data."""
    data = user_input.strip()
    result = []
    
    for item in data.split(','):
        result.append(item.upper())
    
    return result

def calculate_average(numbers):
    total = 0
    count = 0
    
    for num in numbers:
        total += num
        count += 1
    
    return total / count
'''

    print("🔍 Starting Code Review Duo with LangGraph...")
    print(f"📋 Using analyzer config: {analyzer_config_key}")
    print(f"📝 Using documentation config: {documentation_config_key}")
    print()

    # Create the workflow graph with custom state
    workflow = StateGraph(CodeReviewState)
    
    # Add nodes with proper function signatures
    workflow.add_node("analyze", lambda state: ai_node(state, aiclient, context, analyzer_config_key, "analysis", "document"))
    workflow.add_node("document", lambda state: ai_node(state, aiclient, context, documentation_config_key, "documentation", "finalize"))
    workflow.add_node("finalize", create_final_report)
    
    # Define the workflow
    workflow.set_entry_point("analyze")
    
    # Compile the graph
    app = workflow.compile()
    
    # Initialize state with the sample code
    initial_state = {
        "messages": [
            {
                "role": "user",
                "content": sample_code
            }
        ],
        "analysis": "",
        "documentation": "",
        "final_report": ""
    }
    
    # Execute the workflow
    try:
        result = app.invoke(initial_state)
        
        print("\n" + "="*80)
        print("📊 FINAL CODE REVIEW REPORT")
        print("="*80)
        
        # Use the final report from state
        final_report = result.get("final_report", "No report generated")
        print(final_report)
        print("="*80)
        
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        print("Please ensure you have the correct API keys and credentials set up for the detected providers.")

    # Flush pending events and close the client.
    ldclient.get().flush()
    ldclient.get().close()

if __name__ == "__main__":
    main()
