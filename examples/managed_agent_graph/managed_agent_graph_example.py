import os
import logging
from dotenv import load_dotenv
import asyncio
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient

load_dotenv()

logging.basicConfig()
logging.getLogger('ldclient').setLevel(logging.WARNING)

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set graph_key to the Agent Graph key you want to evaluate.
graph_key = os.getenv('LAUNCHDARKLY_AGENT_GRAPH_KEY', 'travel-agent-flow')


def search_flights(destination: str, date: str) -> str:
    """Search for available flights to a destination on a given date."""
    return f"Found 3 flights to {destination} on {date}: Flight A ($400), Flight B ($550), Flight C ($320)."


def search_hotels(destination: str, check_in: str, check_out: str) -> str:
    """Search for available hotels at a destination."""
    return f"Found 2 hotels in {destination}: Hotel Sunrise ($150/night), Hotel Seaside ($220/night)."


def get_weather(city: str) -> str:
    """Get the weather forecast for a given city."""
    return f"The weather in {city} is expected to be sunny with highs around 75°F."


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

    # Set up the evaluation context.
    context = (
        Context
        .builder('example-user-key')
        .kind('user')
        .name('Sandy')
        .build()
    )

    try:
        graph = await aiclient.create_agent_graph(
            graph_key,
            context,
            tools={
                'search_flights': search_flights,
                'search_hotels': search_hotels,
                'get_weather': get_weather,
            },
        )

        if not graph:
            print(f"*** Failed to create agent graph for key: {graph_key}")
            return

        sample_question = 'Plan a trip to Tokyo next week. Find flights, hotels, and check the weather.'
        print(f'\nSending sample question: "{sample_question}"')
        print("Waiting for response...")

        result = await graph.run(sample_question)
        print(f"\nGraph response:\n{result.content}")

        summary = result.metrics
        print("\nGraph metrics:")
        if summary.duration_ms is not None:
            print(f"  Duration:      {summary.duration_ms}ms")
        if summary.success is not None:
            print(f"  Success:       {summary.success}")
        if summary.path:
            print(f"  Path:          {' -> '.join(summary.path)}")
        if summary.usage:
            print(f"  Input tokens:  {summary.usage.input}")
            print(f"  Output tokens: {summary.usage.output}")
            print(f"  Total tokens:  {summary.usage.total}")

        if summary.node_metrics:
            print("\nPer-node metrics:")
            for node_key, node_summary in summary.node_metrics.items():
                print(f"  [{node_key}]")
                if node_summary.duration_ms is not None:
                    print(f"    Duration:      {node_summary.duration_ms}ms")
                if node_summary.success is not None:
                    print(f"    Success:       {node_summary.success}")
                if node_summary.usage:
                    print(f"    Input tokens:  {node_summary.usage.input}")
                    print(f"    Output tokens: {node_summary.usage.output}")
                    print(f"    Total tokens:  {node_summary.usage.total}")
                if node_summary.tool_calls:
                    print(f"    Tool calls:    {', '.join(node_summary.tool_calls)}")

        if result.evaluations is not None:
            eval_results = await result.evaluations

            print("\nJudge results:")
            for eval_result in eval_results:
                print(f"- judge_config_key: {eval_result.judge_config_key}")
                print(f"  sampled: {eval_result.sampled}")
                if not eval_result.sampled:
                    continue
                print(f"  success: {eval_result.success}")
                print(f"  error_message: {eval_result.error_message}")
                print(f"  metric_key: {eval_result.metric_key}")
                print(f"  score: {eval_result.score}")
                print(f"  reasoning: {eval_result.reasoning}")

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
