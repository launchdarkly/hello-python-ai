import os
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient
from ldai_langchain import get_ai_metrics_from_response
from langchain.chat_models import init_chat_model

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

async def async_main():
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

    # Pass a default for improved resiliency when the AI config is unavailable
    # or LaunchDarkly is unreachable; omit for a disabled default.
    # Example:
    #   default = AIConfig(
    #       enabled=True,
    #       model=ModelConfig(name='gpt-4'),
    #       provider=ProviderConfig(name='openai'),
    #       messages=[LDMessage(role='system', content='You are a helpful assistant.')],
    #   )
    #   config_value = aiclient.completion_config(ai_config_key, context, default, {'myUserVariable': "Testing Variable"})
    config_value = aiclient.completion_config(
        ai_config_key,
        context,
        variables={'myUserVariable': "Testing Variable"}
    )
    tracker = config_value.tracker

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
        )
        
        messages = [message.to_dict() for message in (config_value.messages or [])]

        # Add the user input to the conversation
        USER_INPUT = "What can you help me with?"
        print("User Input:\n", USER_INPUT)
        messages.append({'role': 'user', 'content': USER_INPUT})

        # Track the LangChain completion with LaunchDarkly metrics using the LD LangChain provider's extractor
        completion = await tracker.track_metrics_of(
            lambda: llm.ainvoke(messages),
            get_ai_metrics_from_response,
        )
        ai_response = completion.content

        # Add the AI response to the conversation history.
        messages.append({'role': 'assistant', 'content': ai_response})
        print("AI Response:\n", ai_response)

        # Continue the conversation by adding user input to the messages list and invoking the LLM again.
        print("Success.")

    except Exception as e:
        print(f"Error during completion: {e}")
        print("Please ensure you have the correct API keys and credentials set up for the detected provider.")

    # Flush pending events and close the client.
    ldclient.get().flush()
    ldclient.get().close()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
