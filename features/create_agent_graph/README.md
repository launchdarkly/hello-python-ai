# Create Agent Graph Example

This example demonstrates how to use LaunchDarkly's `create_agent_graph` method, which orchestrates multi-node agent workflows with automatic metric tracking at both the graph and per-node level.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create the following configs in your LaunchDarkly project. You can use different keys by setting the environment variables in your `.env`.

   - [Create AI Agent Configs](https://launchdarkly.com/docs/home/ai-configs/agents) for each node in your graph. Configure each with a model and agent instructions. Add tools (e.g. `search_flights`, `search_hotels`, `get_weather`) to the agents that need them.
   - [Create an Agent Graph](https://launchdarkly.com/docs/home/ai-configs/create) that connects your agent configs as nodes with edges defining the workflow. Default key: `sample-agent-graph`.

1. Copy `.env.example` to `.env` and fill in your keys:

   ```bash
   cp .env.example .env
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run agent-graph
```
