# Create Agent Example

This example demonstrates how to use LaunchDarkly's `create_agent` method, which handles model creation, metric tracking, and judge evaluation dispatch automatically.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Agent Config](https://launchdarkly.com/docs/home/ai-configs/agents) with a model and agent instructions. Default key: `sample-agent`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AGENT_KEY=sample-agent
   OPENAI_API_KEY=your-openai-api-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run agent
```
