# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://docs.launchdarkly.com/home/ai-configs/quickstart) or the [Python reference guide](https://docs.launchdarkly.com/sdk/ai/python).

This demo requires Python 3.8 or higher.

## Build Instructions

This repository includes examples for `OpenAI`, `Bedrock`, and `LangChain` for multi-provider support. Depending on your preferred provider, you may have to take some additional steps.

### General setup

1. [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) using the key specified in each example, or copy the key of existing AI Config in your LaunchDarkly project that you want to evaluate.
1. Set the environment variable `LAUNCHDARKLY_SDK_KEY` to your LaunchDarkly SDK key and `LAUNCHDARKLY_AI_CONFIG_KEY` to the AI Config key; otherwise, an AI Config of `sample-ai-config` or `sample-ai-agent-config` will be assumed for most examples.

   ```bash
   export LAUNCHDARKLY_SDK_KEY="1234567890abcdef"
   export LAUNCHDARKLY_AI_CONFIG_KEY="sample-ai-config"
   ```

1. Ensure you have [Poetry](https://python-poetry.org/) installed.

### Provider-Specific Setup

#### OpenAI setup (single provider)

1. Install the required dependencies with `poetry install -E openai` or `poetry install --all-extras`.
1. Set the environment variable `OPENAI_API_KEY` to your OpenAI key.
1. On the command line, run `poetry run openai-example`.

#### Bedrock setup (single provider)

1. Install the required dependencies with `poetry install -E bedrock` or `poetry install --all-extras`.
1. Ensure the required AWS credentials can be [auto-detected by the `boto3` library](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html). Examples might include environment variables, role providers, or shared credential files.
1. On the command line, run `poetry run bedrock-example`.

#### Gemini setup (single provider)

1. Install the required dependencies with `poetry install -E gemini` or `poetry install --all-extras`.
1. Set the environment variable `GOOGLE_API_KEY` to your Google API key.
1. On the command line, run `poetry run gemini-example`.

#### LangChain setup (multiple providers)

This example uses `OpenAI`, `Bedrock`, and `Gemini` LangChain provider packages. You can add additional LangChain providers using the `poetry add` command.

1. Install all dependencies with `poetry install -E langchain` or `poetry install --all-extras`.
1. Set up API keys for the providers you want to use.
1. On the command line, run `poetry run langchain-example`

#### LangGraph setup (multiple providers, single agent)

1. Install all dependencies with `poetry install -E langgraph` or `poetry install --all-extras`.
1. Set up API keys for the providers you want to use.
1. Optionally set environment this variable to use a different agent config:
   ```bash
   export LAUNCHDARKLY_AGENT_CONFIG_KEY="sample-ai-agent-config"
   ```
1. On the command line, run `poetry run langgraph-agent-example`.

#### LangGraph setup (multiple providers, multiple agents)

1. Install all dependencies with `poetry install -E langgraph` or `poetry install --all-extras`.
1. Set up API keys for the providers you want to use.
1. [Create an AI Config (Agent-based)](https://launchdarkly.com/docs/home/ai-configs/agents) using the keys below. Write a goal for each config and enable it with targeting rules.
1. Optionally set these environment variables to use different agent configs:
   ```bash
   export LAUNCHDARKLY_ANALYZER_CONFIG_KEY="code-review-analyzer"
   export LAUNCHDARKLY_DOCUMENTATION_CONFIG_KEY="code-review-documentation"
   ```
1. On the command line, run `poetry run langgraph-multi-agent-example`.
