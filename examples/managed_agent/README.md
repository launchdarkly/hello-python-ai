# Managed Agent Example

This example demonstrates how to use LaunchDarkly's managed agent functionality, which handles model creation, metric tracking, and judge evaluation dispatch automatically.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with an [AI Agent Config](https://launchdarkly.com/docs/home/ai-configs/create) created
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AGENT_CONFIG_KEY=sample-agent-config
   ```

   > `LAUNCHDARKLY_AGENT_CONFIG_KEY` defaults to `sample-agent-config` if not set.

   Add the API key for your chosen provider:

   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

2. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run managed-agent-example
```
