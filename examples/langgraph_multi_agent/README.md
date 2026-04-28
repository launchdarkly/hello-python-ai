# LangGraph Multi-Agent Example (Multiple Agents)

This example demonstrates how to use LaunchDarkly's AI Config with LangGraph to orchestrate multiple agents in a code review workflow.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with [AI Configs (Agent-based)](https://launchdarkly.com/docs/home/ai-configs/agents) created using the keys below. Write a goal for each config and enable it with targeting rules.
- API keys for the providers you want to use

## Setup

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_ANALYZER_CONFIG_KEY=code-review-analyzer
   LAUNCHDARKLY_DOCUMENTATION_CONFIG_KEY=code-review-documentation
   ```

   > `LAUNCHDARKLY_ANALYZER_CONFIG_KEY` defaults to `code-review-analyzer` if not set.
   > `LAUNCHDARKLY_DOCUMENTATION_CONFIG_KEY` defaults to `code-review-documentation` if not set.

   Add the API keys for the providers you want to use:

   ```
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-api-key
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   ```

2. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run langgraph-multi-agent-example
```
