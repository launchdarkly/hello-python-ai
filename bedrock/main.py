import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient
from threading import Event
from halo import Halo
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

# Set this environment variable to skip the loop process and evaluate the AI Config
# a single time.
ci = os.getenv('CI')

def map_prompt_to_conversation(prompt):
    return [
        {
            'role': item.role,
            'content': [{'text': item.content}]
        }
        for item in prompt
    ]

if __name__ == "__main__":
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
    context = Context.builder('example-user-key').kind('user').name('Sandy').build()

    default_value = {
        'model': {
            'modelId': 'my-default-model',
        },
        'enabled': True,
        'myVariable': 'My User Defined Variable'
    }
    
    config_value = aiclient.model_config(ai_config_key, context, default_value, {'myUserVariable': "Testing Variable"})
    tracker = config_value.tracker

    response = tracker.track_bedrock_converse(client.converse(
        modelId=config_value.config.model["modelId"],
        messages=map_prompt_to_conversation(config_value.config.prompt)
    ))

    print("AI Response:", response["output"]["message"]["content"][0]["text"])
    print("Success.")

    if ci is None:
        with Halo(text='Waiting for changes', spinner='dots'):
            try:
                Event().wait()
            except KeyboardInterrupt:
                pass
