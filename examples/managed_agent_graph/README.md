# Managed Agent Graph Example

This example demonstrates how to use LaunchDarkly's managed agent graph functionality, which orchestrates multi-node agent workflows with automatic metric tracking at both the graph and per-node level.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with an [Agent Graph](https://launchdarkly.com/docs/home/ai-configs/create) configured
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AGENT_GRAPH_KEY=travel-agent-flow
   ```

   > `LAUNCHDARKLY_AGENT_GRAPH_KEY` defaults to `travel-agent-flow` if not set.

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
poetry run managed-agent-graph-example
```
