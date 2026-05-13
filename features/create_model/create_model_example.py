import os
import logging
from dotenv import load_dotenv
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AICompletionConfigDefault
from ldobserve import ObservabilityConfig, ObservabilityPlugin

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_COMPLETION_KEY', 'sample-completion')


async def async_main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key, plugins=[
        ObservabilityPlugin(ObservabilityConfig(
            service_name='hello-python-ai-managed-model',
        ))
    ]))

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
            print(f"AI config '{ai_config_key}' is disabled. Verify the config key exists in your LaunchDarkly project and is not targeting a disabled variation.")
            return

        sample_question = 'How can LaunchDarkly help me?'
        print(f'\nSending sample question: "{sample_question}"')
        print("Waiting for response...")

        chat_response = await chat.run(sample_question)
        print(f"\nModel response:\n{chat_response.content}")

        # Judge evaluations run asynchronously. Await them so they complete before the
        # process or request ends—even if you don't need to log or use the results.

        if chat_response.evaluations is not None:
            eval_results = await chat_response.evaluations

            print("Judge results:")
            for result in eval_results:
                print(f"- judge_config_key: {result.judge_config_key}")
                print(f"  sampled: {result.sampled}")
                if not result.sampled:
                    continue
                print(f"  success: {result.success}")
                print(f"  error_message: {result.error_message}")
                print(f"  metric_key: {result.metric_key}")
                print(f"  score: {result.score}")
                print(f"  reasoning: {result.reasoning}")

        else:
            print("\nNo judge evaluations were performed. Try adding a judge to the AI config to see results.")

    except Exception as err:
        # In production, sanitize before logging — provider errors may include credentials.
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
