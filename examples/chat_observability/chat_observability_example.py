import os
from dotenv import load_dotenv
import asyncio
import logging
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AICompletionConfigDefault
from ldobserve import ObservabilityConfig, ObservabilityPlugin

load_dotenv()

logging.getLogger('ldclient').setLevel(logging.WARNING)

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

        user_input_1 = "What is feature flagging in 2 sentences?"
        print("User Input:", user_input_1)
        
        response_1 = await chat.invoke(user_input_1)
        print("Chat Response:", response_1.message.content)

        user_input_2 = "Give me a specific use case example."
        print("\nUser Input:", user_input_2)

        response_2 = await chat.invoke(user_input_2)
        print("Chat Response:", response_2.message.content)

        # Judge evaluations run asynchronously. Await them (e.g. with asyncio.gather) so they
        # complete before the process or request ends—even if you don't need to log or use
        # the results.
        if response_1.evaluations:
            await asyncio.gather(*response_1.evaluations)
        if response_2.evaluations:
            await asyncio.gather(*response_2.evaluations)

        print("\nSuccess.")

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
