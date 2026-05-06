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
logging.getLogger('httpx').setLevel(logging.WARNING)

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

# Service configuration for observability
service_name = os.getenv('SERVICE_NAME', 'hello-python-ai-observability')
service_version = os.getenv('SERVICE_VERSION', '1.0.0')


async def async_main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()


    # Initialize LaunchDarkly SDK with observability plugin
    ldclient.set_config(Config(
        sdk_key,
        plugins=[
            ObservabilityPlugin(
                ObservabilityConfig(
                    service_name=service_name,
                    service_version=service_version,
                )
            )
        ]
    ))

    if not ldclient.get().is_initialized():
        print("\n*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    aiclient = LDAIClient(ldclient.get())
    print("*** SDK successfully initialized")

    # Set up the evaluation context with custom attributes for filtering
    context = (
        Context
        .builder('example-user-key')
        .kind('user')
        .name('Sandy')
        .set('environment', 'observability-demo')
        .set('tier', 'premium')
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
        #   chat = await aiclient.create_model(ai_config_key, context, default, {'example_type': 'observability_demo'})
        chat = await aiclient.create_model(
            ai_config_key,
            context,
            variables={
                'example_type': 'observability_demo',
                'session_id': 'demo-session-123',
                'feature': 'ai_chat'
            }
        )

        if not chat:
            print(f"*** Failed to create chat for key: {ai_config_key}")
            return

        sample_question_1 = "What is feature flagging in 2 sentences?"
        print(f'\nSending sample question: "{sample_question_1}"')
        print("Waiting for response...")

        response_1 = await chat.run(sample_question_1)
        print(f"\nModel response:\n{response_1.content}")

        sample_question_2 = "Give me a specific use case example."
        print(f'\nSending follow-up question: "{sample_question_2}"')
        print("Waiting for response...")

        response_2 = await chat.run(sample_question_2)
        print(f"\nModel response:\n{response_2.content}")

        # Judge evaluations run asynchronously. Await them so they
        # complete before the process or request ends—even if you don't need to log or use
        # the results.
        if response_1.evaluations is not None:
            await response_1.evaluations
        if response_2.evaluations is not None:
            await response_2.evaluations

        print("\nDone! The AI config was evaluated with observability enabled.")

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
