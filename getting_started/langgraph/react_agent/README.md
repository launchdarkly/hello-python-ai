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

1. Copy `.env.example` to `.env` and fill in your keys (only the provider keys for providers you actually use are required):

   ```bash
   cp .env.example .env
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run agent
```
