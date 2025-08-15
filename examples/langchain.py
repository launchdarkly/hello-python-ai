import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, AIConfig, ModelConfig, ProviderConfig, LDMessage
from ldai.tracker import TokenUsage
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

def map_provider_to_langchain(provider_name):
    """Map LaunchDarkly provider names to LangChain provider names."""
    # Add any additional provider mappings here as needed.
    provider_mapping = {
        'gemini': 'google_genai'
    }
    lower_provider = provider_name.lower()
    return provider_mapping.get(lower_provider, lower_provider)

def track_langchain_metrics(tracker, func):
    """
    Track LangChain-specific operations.

    This function will track the duration of the operation, the token
    usage, and the success or error status.

    If the provided function throws, then this method will also throw.

    In the case the provided function throws, this function will record the
    duration and an error.

    A failed operation will not have any token usage data.

    :param tracker: The LaunchDarkly tracker instance.
    :param func: Function to track.
    :return: Result of the tracked function.
    """
    try:
        result = tracker.track_duration_of(func)
        tracker.track_success()
        if hasattr(result, "usage_metadata") and result.usage_metadata:
            # Extract token usage from LangChain response
            usage_data = result.usage_metadata
            token_usage = TokenUsage(
                input=usage_data.get("input_tokens", 0),
                output=usage_data.get("output_tokens", 0),
                total=usage_data.get("total_tokens", 0) # LangChain also has values for input_token_details { cache_creation, cache_read }
            )
            tracker.track_tokens(token_usage)
    except Exception:
        tracker.track_error()
        raise

    return result

def main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not ai_config_key:
        print("*** Please set the LAUNCHDARKLY_AI_CONFIG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    aiclient = LDAIClient(ldclient.get())
    print("*** SDK successfully initialized")

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = (
        Context
        .builder('example-user-key')
        .kind('user')
        .name('Sandy')
        .build()
    )

    DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks."

    # Set a fallback AIConfig to use if a config is not found or your application is not able to connect to LaunchDarkly.
    default_value = AIConfig(
        enabled=True,
        model=ModelConfig(name='gpt-3.5-turbo', parameters={'temperature': 0.7}),  # Default to OpenAI
        provider=ProviderConfig(name='openai'),
        messages=[LDMessage(role='system', content=DEFAULT_SYSTEM_MESSAGE)],
    )

    # Optionally, you can use a disabled AIConfig
    # default_value = AIConfig(
    #     enabled=False
    # )
    
    config_value, tracker = aiclient.config(
        ai_config_key,
        context,
        default_value,
        {'myUserVariable': "Testing Variable"}
    )

    if not config_value.enabled:
        print("AI Config is disabled")
        return

    try:
        # Create LangChain model instance using init_chat_model
        # Map the provider from config_value to LangChain format
        print("Model:", config_value.model.name, "Provider:", config_value.provider.name)
        langchain_provider = map_provider_to_langchain(config_value.provider.name)
        llm = init_chat_model(
            model=config_value.model.name,
            model_provider=langchain_provider,
            temperature=config_value.model.get_parameter('temperature') or 0.7,
            max_tokens=config_value.model.get_parameter('max_tokens') or 1000,
        )
        
        messages = [message.to_dict() for message in (config_value.messages or [])]

        # Add the user input to the conversation
        USER_INPUT = "What can you help me with?"
        print("User Input:\n", USER_INPUT)
        messages.append({'role': 'user', 'content': USER_INPUT})

        # Track the LangChain completion with LaunchDarkly metrics
        completion = track_langchain_metrics(tracker, lambda: llm.invoke(messages))
        ai_response = completion.content

        # Add the AI response to the conversation history.
        messages.append({'role': 'assistant', 'content': ai_response})
        print("AI Response:\n", ai_response)

        # Continue the conversation by adding user input to the messages list and invoking the LLM again.
        print("Success.")

    except Exception as e:
        print(f"Error during completion: {e}")
        print("Please ensure you have the correct API keys and credentials set up for the detected provider.")

    # Close the client to flush events and close the connection.
    ldclient.get().close()


if __name__ == "__main__":
    main()
