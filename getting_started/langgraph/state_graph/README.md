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
poetry run agent-graph
```
