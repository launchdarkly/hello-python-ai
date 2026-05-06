import os
import logging
from dotenv import load_dotenv
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient
from ldai.providers import LDAIMetrics
from ldai_langchain import sum_token_usage_from_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config key for the agent
agent_config_key = os.getenv('LAUNCHDARKLY_AGENT_CONFIG_KEY', 'sample-ai-agent-config')

def map_provider_to_langchain(provider_name):
    """Map LaunchDarkly provider names to LangChain provider names."""
    provider_mapping = {
        'gemini': 'google_genai'
    }
    lower_provider = provider_name.lower()
    return provider_mapping.get(lower_provider, lower_provider)

def get_langgraph_metrics(response):
    """Extract aggregated metrics from a LangGraph agent response."""
    messages = response.get("messages", [])
    return LDAIMetrics(success=True, usage=sum_token_usage_from_messages(messages))

def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is sunny."

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
        .builder('weather-user')
        .kind('user')
        .name('Weather User')
        .build()
    )

    print(f"\nUsing agent config: {agent_config_key}")

    # Pass a default for improved resiliency when the agent config is unavailable
    # or LaunchDarkly is unreachable; omit for a disabled default.
    # Example (enabled default):
    #   default = AIAgentConfigDefault(
    #       enabled=True,
    #       instructions='You are a helpful assistant.',
    #   )
    #   agent_config = aiclient.agent_config(agent_config_key, context, default=default)
    agent_config = aiclient.agent_config(agent_config_key, context)

    if not agent_config.enabled:
        print("AI Agent Config is disabled")
        return
    
    langchain_provider = map_provider_to_langchain(agent_config.provider.name)
    llm = init_chat_model(
        model=agent_config.model.name,
        model_provider=langchain_provider,
    )
    
    # Create a React agent with the LLM and tools
    agent = create_react_agent(
        model=llm,
        tools=[get_weather],
        prompt=agent_config.instructions
    )

    SAMPLE_QUESTION = "What is the weather in Tokyo?"

    print(f'\nSending sample question to {agent_config.model.name} agent: "{SAMPLE_QUESTION}"')
    print("Waiting for response...")

    try:
        tracker = agent_config.create_tracker()
        response = tracker.track_metrics_of(
            get_langgraph_metrics,
            lambda: agent.invoke({
                "messages": [{"role": "user", "content": SAMPLE_QUESTION}]
            }),
        )

        print(f"\nAgent response:\n{response['messages'][-1].content}")

        summary = tracker.get_summary()
        print("\nDone! The agent config was evaluated and the following metrics were tracked:")
        print(f"  Duration:      {summary.duration_ms}ms")
        print(f"  Success:       {summary.success}")
        if summary.usage:
            print(f"  Input tokens:  {summary.usage.input}")
            print(f"  Output tokens: {summary.usage.output}")
            print(f"  Total tokens:  {summary.usage.total}")
        if summary.tool_calls:
            print(f"  Tool calls:    {', '.join(summary.tool_calls)}")

    except Exception as e:
        print(f"\nError: {e}")
        print("Please ensure you have the correct API keys and credentials set up for the detected providers.")

    # Flush pending events and close the client.
    ldclient.get().flush()
    ldclient.get().close()

if __name__ == "__main__":
    main()
