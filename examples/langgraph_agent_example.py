import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, ModelConfig, ProviderConfig, LDMessage, LDAIAgentConfig, LDAIAgentDefaults
from ldai.tracker import TokenUsage
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from typing import Annotated, Sequence, Literal
from typing_extensions import TypedDict
import json

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

    print(f"🔍 Using agent config: {agent_config_key}")
    print()

    """Create a LangChain model with LaunchDarkly AI config."""
    # Default value with disabled agent
    default_value = LDAIAgentDefaults(
        enabled=False,  # Disabled by default
    )

    agent_config = aiclient.agent(
        LDAIAgentConfig(
            key=agent_config_key,
            default_value=default_value,
        ),
        context
    )

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

    try:
        # Track and execute the agent
        response = track_langchain_metrics(agent_config.tracker, lambda: agent.invoke({
            "messages": [{"role": "user", "content": "What is the weather in Tokyo?"}]
        }))
        
        print("Agent response:")
        print(response["messages"][-1].content)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure you have the correct API keys and credentials set up for the detected providers.")

    # Close the client to flush events and close the connection.
    ldclient.get().close()

if __name__ == "__main__":
    main()
