import os
import logging
from dotenv import load_dotenv
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient
from ldai_openai import get_ai_metrics_from_response
from openai import OpenAI

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

openai_client = OpenAI()

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')


def main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not ai_config_key:
        print("*** Please set the LAUNCHDARKLY_AI_CONFIG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    aiclient = LDAIClient(ldclient.get())

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

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

    messages = [message.to_dict() for message in (config_value.messages or [])]

    SAMPLE_QUESTION = "What can you help me with?"
    messages.append({'role': 'user', 'content': SAMPLE_QUESTION})

    print(f'\nSending sample question to {config_value.model.name}: "{SAMPLE_QUESTION}"')
    print("Waiting for response...")

    completion = tracker.track_metrics_of(
        get_ai_metrics_from_response,
        lambda:
            openai_client.chat.completions.create(
                model=config_value.model.name,
                messages=messages,
            ),
    )
    ai_response = completion.choices[0].message.content

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

    # Flush pending events and close the client.
    ldclient.get().flush()
    ldclient.get().close()
