import os
import logging
from dotenv import load_dotenv
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient
from ldai_langchain import get_ai_metrics_from_response
from langchain.chat_models import init_chat_model

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

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

    if not config_value.enabled:
        print("AI Config is disabled")
        return

    tracker = config_value.create_tracker()

    try:
        langchain_provider = map_provider_to_langchain(config_value.provider.name)
        llm = init_chat_model(
            model=config_value.model.name,
            model_provider=langchain_provider,
        )

        messages = [message.to_dict() for message in (config_value.messages or [])]

        SAMPLE_QUESTION = "What can you help me with?"
        messages.append({'role': 'user', 'content': SAMPLE_QUESTION})

        print(f'\nSending sample question to {config_value.model.name} via LangChain ({langchain_provider}): "{SAMPLE_QUESTION}"')
        print("Waiting for response...")

        completion = await tracker.track_metrics_of_async(
            get_ai_metrics_from_response,
            lambda: llm.ainvoke(messages),
        )
        ai_response = completion.content

        messages.append({'role': 'assistant', 'content': ai_response})

        print(f"\nModel response:\n{ai_response}")

        summary = tracker.get_summary()
        print("\nDone! The AI config was evaluated and the following metrics were tracked:")
        print(f"  Duration:      {summary.duration_ms}ms")
        print(f"  Success:       {summary.success}")
        if summary.usage:
            print(f"  Input tokens:  {summary.usage.input}")
            print(f"  Output tokens: {summary.usage.output}")
            print(f"  Total tokens:  {summary.usage.total}")
        if summary.tool_calls:
            print(f"  Tool calls:    {', '.join(summary.tool_calls)}")

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
