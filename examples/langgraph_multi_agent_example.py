import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, ModelConfig, ProviderConfig, LDMessage, LDAIAgentConfig, LDAIAgentDefaults
from ldai.tracker import TokenUsage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from typing import Annotated, Sequence, Literal
from typing_extensions import TypedDict
import json

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

def track_langchain_metrics(tracker, func):
    """
    Track LangChain-specific operations with LaunchDarkly metrics.
    """
    try:
        result = tracker.track_duration_of(func)
        tracker.track_success()
        if hasattr(result, "usage_metadata") and result.usage_metadata:
            usage_data = result.usage_metadata
            token_usage = TokenUsage(
                input=usage_data.get("input_tokens", 0),
                output=usage_data.get("output_tokens", 0),
                total=usage_data.get("total_tokens", 0)
            )
            tracker.track_tokens(token_usage)
    except Exception:
        tracker.track_error()
        raise
    return result

# Agent system prompts
ANALYZER_AGENT_INSTRUCTIONS = """You are a senior software engineer specializing in code review and analysis. Your role is to thoroughly analyze code for:

1. **Bug Detection**: Identify potential bugs, logic errors, and edge cases
2. **Performance Issues**: Spot inefficient algorithms, memory leaks, and optimization opportunities
3. **Security Vulnerabilities**: Detect security flaws like SQL injection, XSS, authentication issues
4. **Code Quality**: Assess readability, maintainability, and adherence to best practices
5. **Architecture Concerns**: Identify design patterns, coupling issues, and scalability problems

**Analysis Guidelines:**
- Be thorough but constructive in your feedback
- Provide specific examples and suggestions for improvements
- Consider the programming language's best practices
- Prioritize issues by severity (critical, high, medium, low)
- Include both problems and positive observations

**Output Format:**
- Use markdown formatting to organize the results
- Indent any headings to fit under the "## Code Analysis"
- Start with a brief summary of overall code quality
- List issues by category (Bugs, Performance, Security, Quality, Architecture)
- For each issue, provide: severity, description, location, and suggested fix
- End with recommendations for next steps"""

DOCUMENTATION_AGENT_INSTRUCTIONS = """You are a technical writer specializing in software documentation. Your role is to create clear, comprehensive documentation based on code analysis and review feedback.

**Documentation Responsibilities:**
1. **Function Documentation**: Create clear docstrings and function descriptions
2. **API Documentation**: Document interfaces, parameters, and return values
3. **Usage Examples**: Provide practical examples of how to use the code
4. **Troubleshooting Guides**: Document common issues and solutions
5. **README Updates**: Suggest improvements to project documentation

**Writing Guidelines:**
- Use clear, concise language that both technical and non-technical stakeholders can understand
- Include code examples where helpful
- Structure documentation logically with headers and sections
- Consider the target audience (developers, users, maintainers)
- Follow documentation best practices for the specific technology stack

**Output Format:**
- The results will be included in an existing markdown document section titled ## Generated Documentation
- Generate appropriate docstrings for functions/classes
- Create usage examples and code snippets
- Suggest README improvements
- Provide troubleshooting sections if issues were identified
- Include any relevant diagrams or flow descriptions"""

def create_agent_with_config(aiclient, config_key, context, agent_instructions):
    """Create a LangChain model with LaunchDarkly AI config."""
    default_value = LDAIAgentDefaults(
        enabled=True,
        model=ModelConfig(name='gpt-3.5-turbo', parameters={}),
        provider=ProviderConfig(name='openai'),
        instructions=agent_instructions,
    )

    agent_config = aiclient.agent(
        LDAIAgentConfig(
            key=config_key,
            default_value=default_value,
        ),
        context
    )

    if not agent_config.enabled:
        raise Exception(f"AI Config {config_key} is disabled")
    
    langchain_provider = map_provider_to_langchain(agent_config.provider.name)
    llm = init_chat_model(
        model=agent_config.model.name,
        model_provider=langchain_provider,
    )
    
    # Create a React agent with the LLM
    agent = create_react_agent(llm, [], prompt=agent_config.instructions)
    
    return agent, agent_config.tracker

def analyze_code(state: CodeReviewState, aiclient, context) -> Command[Literal["document", END]]:
    """Agent that analyzes code for issues and improvements."""
    print("Analyzing code")
    try:
        agent, tracker = create_agent_with_config(
            aiclient, analyzer_config_key, context, ANALYZER_AGENT_INSTRUCTIONS
        )
        
        # Track and execute the analysis
        completion = track_langchain_metrics(tracker, lambda: agent.invoke({"messages": state["messages"]}))
        
        print(f"✅ Code analysis completed using {analyzer_config_key}")
        
        # Extract the analysis from the agent's response
        analysis = ""
        if completion["messages"]:
            last_message = completion["messages"][-1]
            if hasattr(last_message, 'content'):
                analysis = last_message.content
            else:
                analysis = last_message.get('content', '')
        
        # Return Command to update state and route to next agent
        return Command(
            goto="document",
            update={
                "messages": completion["messages"],
                "analysis": analysis
            }
        )
        
    except Exception as e:
        print(f"❌ Error in code analysis: {e}")
        return Command(
            goto=END,
            update={
                "messages": [{"role": "system", "content": f"Error: {str(e)}"}],
                "analysis": f"Error: {str(e)}"
            }
        )

def generate_documentation(state: CodeReviewState, aiclient, context) -> Command[Literal["finalize", END]]:
    """Agent that generates documentation based on code analysis."""
    print("Generating documentation")
    try:
        agent, tracker = create_agent_with_config(
            aiclient, documentation_config_key, context, DOCUMENTATION_AGENT_INSTRUCTIONS
        )
    
        # Create context message with the analysis
        context_message = f"Based on this code analysis:\n\n{state['analysis']}\n\nPlease generate comprehensive documentation."
        messages_with_context = state["messages"] + [{"role": "user", "content": context_message}]
        
        # Track and execute the documentation generation
        completion = track_langchain_metrics(tracker, lambda: agent.invoke({"messages": messages_with_context}))
        
        print(f"✅ Documentation generated using {documentation_config_key}")
        
        # Extract the documentation from the agent's response
        documentation = ""
        if completion["messages"]:
            last_message = completion["messages"][-1]
            if hasattr(last_message, 'content'):
                documentation = last_message.content
            else:
                documentation = last_message.get('content', '')
        
        # Return Command to update state and route to next agent
        return Command(
            goto="finalize",
            update={
                "messages": completion["messages"],
                "documentation": documentation
            }
        )
        
    except Exception as e:
        print(f"❌ Error in documentation generation: {e}")
        return Command(
            goto=END,
            update={
                "messages": [{"role": "system", "content": f"Error: {str(e)}"}],
                "documentation": f"Error: {str(e)}"
            }
        )

def create_final_report(state: CodeReviewState) -> Command[Literal[END]]:
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
    workflow.add_node("analyze", lambda state: analyze_code(state, aiclient, context))
    workflow.add_node("document", lambda state: generate_documentation(state, aiclient, context))
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

    # Close the client to flush events and close the connection.
    ldclient.get().close()

if __name__ == "__main__":
    main()
