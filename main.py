import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient
from ldai.types import OpenAITokenUsage
from threading import Event
from halo import Halo
from openai import OpenAI

openai_client = OpenAI()

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

# Set this environment variable to skip the loop process and evaluate the AI Config
# a single time.
ci = os.getenv('CI')


if __name__ == "__main__":
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not ai_config_key:
        print("*** Please set the LAUNCHDARKLY_AI_CONFIG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    aiClient = LDAIClient(ldclient.get())
    
    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = Context.builder('example-user-key').kind('user').name('Sandy').build()

    
    configValue = aiClient.model_config(ai_config_key, context, False, {'myUserVariable': "Testing Variable"})
    tracker = configValue.tracker

    completion = tracker.track_openai(openai_client.chat.completions.create,
    model=configValue.config["config"]["modelId"],
    messages=configValue.config["prompt"]
    )

    print("AI Response:", completion.choices[0].message.content)
    print("Success.")

    if ci is None:
        with Halo(text='Waiting for changes', spinner='dots'):
            try:
                Event().wait()
            except KeyboardInterrupt:
                pass