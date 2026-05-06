# LangGraph Multi-Agent Example (Multiple Agents)

This example demonstrates how to use LaunchDarkly's AI Config with LangGraph to orchestrate multiple agents in a code review workflow.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the providers you want to use

## Setup

1. Create the following configs in your LaunchDarkly project. You can use different keys by setting the environment variables in your `.env`.

   - [Create an AI Agent Config](https://launchdarkly.com/docs/home/ai-configs/agents) for code analysis. Default key: `code-review-analyzer`.
   - [Create an AI Agent Config](https://launchdarkly.com/docs/home/ai-configs/agents) for documentation generation. Default key: `code-review-documentation`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_ANALYZER_CONFIG_KEY=code-review-analyzer
   LAUNCHDARKLY_DOCUMENTATION_CONFIG_KEY=code-review-documentation
   ```

   Add the API keys for the providers you want to use:

   ```
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-api-key
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run langgraph-multi-agent-example
```
