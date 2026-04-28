# LangGraph Agent Example (Single Agent)

This example demonstrates how to use LaunchDarkly's AI Config with LangGraph to create a single ReAct agent with tool support.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with an [AI Config (Agent-based)](https://launchdarkly.com/docs/home/ai-configs/agents) created
- API keys for the providers you want to use

## Setup

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AGENT_CONFIG_KEY=sample-ai-agent-config
   ```

   > `LAUNCHDARKLY_AGENT_CONFIG_KEY` defaults to `sample-ai-agent-config` if not set.

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
poetry run langgraph-agent-example
```
