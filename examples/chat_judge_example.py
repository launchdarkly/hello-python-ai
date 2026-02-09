import os
import json
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AICompletionConfigDefault

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
        # Example using the chat functionality which automates the judge evaluation
        default_value = AICompletionConfigDefault(
            enabled=False,
        )

        chat = await aiclient.create_chat(ai_config_key, context, default_value, {
            'companyName': 'LaunchDarkly',
        })

        if not chat:
            print(f"*** AI chat configuration is not enabled for key: {ai_config_key}")
            return

        print("\n*** Starting chat with automatic judge evaluation:")
        user_input = 'How can LaunchDarkly help me?'
        print("User Input:", user_input)

        # The invoke method will automatically evaluate the chat response with any judges defined in the AI config
        chat_response = await chat.invoke(user_input)
        print("Chat Response:", chat_response.message.content)

        # Log judge evaluation results with full detail
        if chat_response.evaluations is not None and len(chat_response.evaluations) > 0:
            # Note: Judge evaluations run asynchronously and do not block your application.
            # Results are automatically sent to LaunchDarkly for AI config metrics.
            # You only need to await if you want to access the evaluation results in your code.
            print("\nNote: Awaiting judge results (optional - done here for demonstration only).")
            eval_results = await asyncio.gather(*chat_response.evaluations)
            
            # Convert results, replacing None with a message
            results_to_display = [
                result.to_dict() if result is not None else "not evaluated" 
                for result in eval_results
            ]
            
            print("Judge results:")
            print(json.dumps(results_to_display, indent=2, default=str))
            
            if None in eval_results:
                print("\nNote: Some judge evaluations were skipped.")
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
        # Close the client to flush events and close the connection.
        ldclient.get().close()


def main():
    """Synchronous entry point for Poetry script."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
