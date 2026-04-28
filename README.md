# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://docs.launchdarkly.com/home/ai-configs/quickstart) or the [Python reference guide](https://docs.launchdarkly.com/sdk/ai/python).

This demo requires Python 3.10 or higher.

## Build Instructions

This repository includes examples for `OpenAI`, `Bedrock`, `Gemini`, `LangChain`, `LangGraph`, `Judge`, and `Observability`. Depending on your preferred provider, you may have to take some additional steps.

### General setup

1. [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) using the key specified in each example, or copy the key of existing AI Config in your LaunchDarkly project that you want to evaluate.

1. Ensure you have [Poetry](https://python-poetry.org/) installed.

1. Create a `.env` file in the repository root with at least your LaunchDarkly SDK key:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   ```

   Each example README describes the full set of environment variables needed. The `.env` file is loaded automatically when running any example.

### Examples

| Example | Description | README |
| --- | --- | --- |
| **OpenAI** | Single provider using OpenAI | [examples/openai](examples/openai/README.md) |
| **Bedrock** | Single provider using AWS Bedrock | [examples/bedrock](examples/bedrock/README.md) |
| **Gemini** | Single provider using Google Gemini | [examples/gemini](examples/gemini/README.md) |
| **LangChain** | Multiple providers via LangChain | [examples/langchain](examples/langchain/README.md) |
| **LangGraph Agent** | Single agent using LangGraph | [examples/langgraph_agent](examples/langgraph_agent/README.md) |
| **LangGraph Multi-Agent** | Multiple agents using LangGraph | [examples/langgraph_multi_agent](examples/langgraph_multi_agent/README.md) |
| **Judge** | Judge evaluation of AI responses | [examples/judge](examples/judge/README.md) |
| **Chat with Observability** | Observability plugin for AI chat monitoring | [examples/chat_observability](examples/chat_observability/README.md) |
