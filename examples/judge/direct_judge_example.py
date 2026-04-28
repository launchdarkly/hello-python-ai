import os
from dotenv import load_dotenv
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AIJudgeConfigDefault

load_dotenv()

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set judge_key to the Judge key you want to use.
judge_key = os.getenv('LAUNCHDARKLY_AI_JUDGE_KEY', 'sample-ai-judge')


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
        # Pass a default for improved resiliency when the AI config is unavailable
        # or LaunchDarkly is unreachable; omit for a disabled default.
        # Example (enabled default; judge default has three messages):
        #   default = AIJudgeConfigDefault(
        #       enabled=True,
        #       model={'name': 'gpt-4'},
        #       provider={'name': 'openai'},
        #       messages=[
        #           {'role': 'system', 'content': 'Your judge criteria here.'},
        #           {'role': 'assistant', 'content': 'MESSAGE HISTORY: {{message_history}}'},
        #           {'role': 'user', 'content': 'RESPONSE TO EVALUATE: {{response_to_evaluate}}'},
        #       ],
        #   )
        #   judge = aiclient.create_judge(judge_key, context, default)
        judge = aiclient.create_judge(judge_key, context)

        if not judge:
            print(f"*** Failed to create judge for key: {judge_key}")
            return

        print("\n*** Starting direct judge evaluation of input and output:")
        input_text = 'You are a helpful assistant for the company LaunchDarkly. How can you help me?'
        output_text = 'I can answer any question you have except for questions about the company LaunchDarkly.'

        print("Input:", input_text)
        print("Output:", output_text)

        judge_response = await judge.evaluate(input_text, output_text)

        # Track the judge evaluation scores on the tracker for the aiConfig you are evaluating
        # Example:
        # aiConfig.tracker.track_eval_scores(judge_response.evals)

        print("Judge Response:")
        print(f"  sampled: {judge_response.sampled}")
        print(f"  success: {judge_response.success}")
        if judge_response.error_message is not None:
            print(f"  error_message: {judge_response.error_message}")
        if judge_response.metric_key is not None:
            print(f"  metric_key: {judge_response.metric_key}")
        if judge_response.score is not None:
            print(f"  score: {judge_response.score}")
        if judge_response.reasoning is not None:
            print(f"  reasoning: {judge_response.reasoning}")

        if not judge_response.sampled:
            print("\nNote: Judge evaluation was not sampled.")
            print("This typically happens when the sample rate doesn't require this evaluation, or due to a configuration issue.")
            print("Check application logs for more details.")

        print("Success.")
    except Exception as err:
        print("Error:", err)
    finally:
        # Flush pending events and close the client.
        ldclient.get().flush()
        ldclient.get().close()


def main():
    """Synchronous entry point for Poetry script."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
