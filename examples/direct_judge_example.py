import os
import json
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AICompletionConfigDefault

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set judge_key to the Judge key you want to use.
judge_key = os.getenv('LAUNCHDARKLY_AI_JUDGE_KEY', 'sample-ai-judge-accuracy')


async def async_main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
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

    try:
        # Example of using the judge functionality with direct input and output
        # Get AI judge configuration from LaunchDarkly
        judge_default_value = AICompletionConfigDefault(
            enabled=False,
        )
        judge = await aiclient.create_judge(judge_key, context, judge_default_value)

        if not judge:
            print(f"*** AI judge configuration is not enabled for key: {judge_key}")
            return

        print("\n*** Starting direct judge evaluation of input and output:")
        input_text = 'You are a helpful assistant for the company LaunchDarkly. How can you help me?'
        output_text = 'I can answer any question you have except for questions about the company LaunchDarkly.'

        print("Input:", input_text)
        print("Output:", output_text)

        judge_response = await judge.evaluate(input_text, output_text)

        if judge_response is None:
            print("\nJudge evaluation was skipped.")
            print("This typically happens when the sample rate doesn't require this evaluation, or due to a configuration issue.")
            print("Check application logs for more details.")
            return

        # Track the judge evaluation scores on the tracker for the aiConfig you are evaluating
        # Example:
        # aiConfig.tracker.track_eval_scores(judge_response.evals)

        # Convert JudgeResponse to dict for display using to_dict()
        judge_response_dict = judge_response.to_dict()
        print("Judge Response:")
        print(json.dumps(judge_response_dict, indent=2, default=str))

        print("Success.")
    except Exception as err:
        print("Error:", err)
    finally:
        # Close the client to flush events and close the connection.
        ldclient.get().close()


def main():
    """Synchronous entry point for Poetry script."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
