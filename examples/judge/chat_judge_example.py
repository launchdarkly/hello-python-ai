import os
from dotenv import load_dotenv
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AICompletionConfigDefault

load_dotenv()

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')


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
        # Example:
        #   default = AICompletionConfigDefault(
        #       enabled=True,
        #       model={'name': 'gpt-4'},
        #       provider={'name': 'openai'},
        #       messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}],
        #   )
        #   chat = await aiclient.create_model(ai_config_key, context, default, {'companyName': 'LaunchDarkly'})
        chat = await aiclient.create_model(ai_config_key, context, variables={
            'companyName': 'LaunchDarkly',
        })

        if not chat:
            print(f"*** Failed to create chat for key: {ai_config_key}")
            return

        print("\n*** Starting chat with automatic judge evaluation:")
        user_input = 'How can LaunchDarkly help me?'
        print("User Input:", user_input)

        # The run method will automatically evaluate the chat response with any judges defined in the AI config
        chat_response = await chat.run(user_input)
        print("Chat Response:", chat_response.content)

        # Judge evaluations run asynchronously. Await them so they complete before the
        # process or request ends—even if you don't need to log or use the results.
        # Below we await and then log the results for demonstration.

        # Log judge evaluation results with full detail
        if chat_response.evaluations is not None:
            # Note: Judge evaluations run asynchronously and do not block your application.
            # Results are automatically sent to LaunchDarkly for AI config metrics.
            # You only need to await if you want to access the evaluation results in your code.
            print("\nNote: Awaiting judge results (optional - done here for demonstration only).")
            eval_results = await chat_response.evaluations

            print("Judge results:")
            for result in eval_results:
                print(f"  - sampled: {result.sampled}")
                print(f"    success: {result.success}")
                if result.error_message is not None:
                    print(f"    error_message: {result.error_message}")
                if result.metric_key is not None:
                    print(f"    metric_key: {result.metric_key}")
                if result.score is not None:
                    print(f"    score: {result.score}")
                if result.reasoning is not None:
                    print(f"    reasoning: {result.reasoning}")

            skipped = [r for r in eval_results if not r.sampled]
            if skipped:
                print("\nNote: Some judge evaluations were skipped (not sampled).")
                print("This typically happens when the sample rate doesn't require this evaluation, or due to a configuration issue.")
                print("Check application logs for more details.")
        else:
            print("\nNo judge evaluations were performed.")
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
