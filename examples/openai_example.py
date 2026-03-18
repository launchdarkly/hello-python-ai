import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient
from openai import OpenAI

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
    tracker = config_value.tracker

    if not config_value.enabled:
        print("AI Config is disabled")
        return
    
    messages = [message.to_dict() for message in (config_value.messages or [])]

    # Add the user input to the conversation
    USER_INPUT = "What can you help me with?"
    print("User Input:\n", USER_INPUT)
    messages.append({'role': 'user', 'content': USER_INPUT})

    # Track the OpenAI completion with LaunchDarkly metrics
    completion = tracker.track_openai_metrics(
        lambda:
            openai_client.chat.completions.create(
                model=config_value.model.name,
                messages=messages,
            )
    )
    ai_response = completion.choices[0].message.content

    # Add the AI response to the conversation history.
    messages.append({'role': 'assistant', 'content': ai_response})
    print("AI Response:\n", ai_response)

    # Continue the conversation by adding user input to the messages list and invoking the LLM again.
    print("Success.")

    # Close the client to flush events and close the connection.
    ldclient.get().close()
