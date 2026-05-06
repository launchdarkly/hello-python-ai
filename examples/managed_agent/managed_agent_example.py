import os
import logging
from dotenv import load_dotenv
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AIAgentConfigDefault

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set agent_config_key to the AI Agent Config key you want to evaluate.
agent_config_key = os.getenv('LAUNCHDARKLY_AGENT_CONFIG_KEY', 'sample-agent-config')


def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is sunny."


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
        # Pass a default for improved resiliency when the agent config is unavailable
        # or LaunchDarkly is unreachable; omit for a disabled default.
        # Example:
        #   default = AIAgentConfigDefault(
        #       enabled=True,
        #       model={'name': 'gpt-4'},
        #       provider={'name': 'openai'},
        #       instructions='You are a helpful weather assistant.',
        #   )
        #   agent = await aiclient.create_agent(agent_config_key, context, tools={'get_weather': get_weather}, default=default)
        agent = await aiclient.create_agent(
            agent_config_key,
            context,
            tools={'get_weather': get_weather},
        )

        if not agent:
            print(f"*** Failed to create agent for key: {agent_config_key}")
            return

        sample_question = 'What is the weather in Tokyo?'
        print(f'\nSending sample question: "{sample_question}"')
        print("Waiting for response...")

        agent_response = await agent.run(sample_question)
        print(f"\nAgent response:\n{agent_response.content}")

        summary = agent_response.metrics
        print("\nMetrics tracked:")
        print(f"  Duration:      {summary.duration_ms}ms")
        print(f"  Success:       {summary.success}")
        if summary.usage:
            print(f"  Input tokens:  {summary.usage.input}")
            print(f"  Output tokens: {summary.usage.output}")
            print(f"  Total tokens:  {summary.usage.total}")
        if summary.tool_calls:
            print(f"  Tool calls:    {', '.join(summary.tool_calls)}")

        if agent_response.evaluations is not None:
            eval_results = await agent_response.evaluations

            print("\nJudge results:")
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
            print("\nNo judge evaluations were performed.")

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
