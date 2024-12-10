import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, AIConfig, ModelConfig
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
    context = Context.builder(
        'example-user-key').kind('user').name('Sandy').build()

    default_value = AIConfig(
        enabled=True,
        model=ModelConfig(name='my-default-model'),
        messages=[],
    )
    config_value, tracker = aiclient.config(
        ai_config_key,
        context,
        default_value,
        {'myUserVariable': "Testing Variable"}
    )

    completion = tracker.track_openai_metrics(
        openai_client.chat.completions.create(
            model=config_value.model.name,
            messages=[message.to_json() for message in config_value.messages],
        )
    )

    print("AI Response:", completion.choices[0].message.content)
    print("Success.")

    # Close the client to flush events and close the connection.
    ldclient.get().close()
