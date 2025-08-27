import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, AIConfig, ModelConfig, ProviderConfig, LDMessage
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

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

    DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks."

    # Set a fallback AIConfig to use if a config is not found or your application is not able to connect to LaunchDarkly.
    default_value = AIConfig(
        enabled=True,
        model=ModelConfig(name='my-default-model', parameters={}),
        provider=ProviderConfig(name='bedrock'),
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

    # Map the messages to the format expected by Bedrock
    chat_messages = [{'role': msg.role, 'content': [{'text': msg.content}]} for msg in config_value.messages if msg.role != 'system']
    system_messages = [{'text': msg.content} for msg in config_value.messages if msg.role == 'system']

    # Add the user input to the conversation
    USER_INPUT = "What can you help me with?"
    print("User Input:\n", USER_INPUT)
    chat_messages.append({'role': 'user', 'content': [{'text': USER_INPUT}]})

    converse = tracker.track_bedrock_converse_metrics(
        client.converse(
            modelId=config_value.model.name,
            messages=chat_messages,
            system=system_messages,
        )
    )

    # Append the AI response to the conversation history
    chat_messages.append(converse["output"]["message"])
    print("AI Response:\n", converse["output"]["message"]["content"][0]["text"])

    # Continue the conversation by adding user input to the messages list and invoking the LLM again.
    print("Success.")

    # Close the client to flush events and close the connection.
    ldclient.get().close()
