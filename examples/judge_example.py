import os
import json
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

# Set judge_key to the Judge key you want to use.
judge_key = os.getenv('LAUNCHDARKLY_JUDGE_KEY', 'ld-ai-judge-accuracy')


def main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    aiclient = LDAIClient(ldclient.get())

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the context properties. This context should appear on your LaunchDarkly contexts dashboard
    # soon after you run the demo.
    context = (
        Context
        .builder('example-user-key')
        .kind('user')
        .name('Sandy')
        .build()
    )

    try:
        # Example using the chat functionality which automates the judge evaluation
        default_value = {
            'enabled': False,
        }

        chat = aiclient.create_chat(ai_config_key, context, default_value, {
            'companyName': 'LaunchDarkly',
        })

        if not chat:
            print("*** AI chat configuration is not enabled")
            return

        print("\n*** Starting chat:")
        user_input = 'How can LaunchDarkly help me?'
        print("User Input:", user_input)

        # The invoke method will automatically evaluate the chat response with any judges defined in the AI config
        chat_response = chat.invoke(user_input)
        print("Chat Response:", chat_response.message.content)

        # Log judge evaluation results with full detail
        eval_results = chat_response.evaluations
        print("Judge results:", json.dumps(eval_results, indent=2))

        # Example of using the judge functionality with direct input and output
        # Get AI judge configuration from LaunchDarkly
        judge = aiclient.create_judge(judge_key, context, {'enabled': False})

        if not judge:
            print("*** AI judge configuration is not enabled")
            return

        print("\n*** Starting judge evaluation of direct input and output:")
        input_text = 'You are a helpful assistant for the company LaunchDarkly. How can you help me?'
        output_text = 'I can answer any question you have except for questions about the company LaunchDarkly.'

        print("Input:", input_text)
        print("Output:", output_text)

        judge_response = judge.evaluate(input_text, output_text)

        # Track the judge evaluation scores on the tracker for the aiConfig you are evaluating
        # Example:
        # aiConfig.tracker.track_eval_scores(judge_response.evals)

        print("Judge Response:", judge_response)

        print("Success.")

    except Exception as err:
        print("Error:", err)

    # Close the client to flush events and close the connection.
    ldclient.get().close()


if __name__ == "__main__":
    main()

