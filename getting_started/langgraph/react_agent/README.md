# LangGraph Agent Example (Single Agent)

This example demonstrates how to use LaunchDarkly's AI Config with LangGraph to create a single ReAct agent with tool support.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the providers you want to use

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Agent Config](https://launchdarkly.com/docs/home/ai-configs/agents) with a model and agent instructions. Default key: `sample-agent`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AGENT_KEY=sample-agent
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
poetry run agent
```
