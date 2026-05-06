import os
import logging
from dotenv import load_dotenv
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient
from ldai.tracker import TokenUsage
from ldai.providers import LDAIMetrics
import boto3

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

client = boto3.client("bedrock-runtime", region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1'))


def get_bedrock_metrics(response):
    """Extract metrics from a Bedrock converse response."""
    status_code = response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0)
    success = status_code == 200

    usage = None
    if response.get("usage"):
        u = response["usage"]
        usage = TokenUsage(
            total=u.get("totalTokens", 0),
            input=u.get("inputTokens", 0),
            output=u.get("outputTokens", 0),
        )

    duration_ms = response.get("metrics", {}).get("latencyMs")

    return LDAIMetrics(success=success, usage=usage, duration_ms=duration_ms)

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
    #       model=ModelConfig(name='my-default-model'),
    #       provider=ProviderConfig(name='bedrock'),
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

    # Map the messages to the format expected by Bedrock
    chat_messages = [{'role': msg.role, 'content': [{'text': msg.content}]} for msg in config_value.messages if msg.role != 'system']
    system_messages = [{'text': msg.content} for msg in config_value.messages if msg.role == 'system']

    SAMPLE_QUESTION = "What can you help me with?"
    chat_messages.append({'role': 'user', 'content': [{'text': SAMPLE_QUESTION}]})

    print(f'\nSending sample question to {config_value.model.name}: "{SAMPLE_QUESTION}"')
    print("Waiting for response...")

    converse = tracker.track_metrics_of(
        get_bedrock_metrics,
        lambda: client.converse(
            modelId=config_value.model.name,
            messages=chat_messages,
            system=system_messages,
        ),
    )

    chat_messages.append(converse["output"]["message"])

    print(f"\nModel response:\n{converse['output']['message']['content'][0]['text']}")

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
