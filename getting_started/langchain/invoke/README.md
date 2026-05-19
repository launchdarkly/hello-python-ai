# LangChain Example (Multiple Providers)

This example demonstrates how to use LaunchDarkly's AI Config with LangChain, supporting multiple providers including OpenAI, Anthropic, Google GenAI, and AWS Bedrock. To use a different provider, install the corresponding `langchain-*` package (e.g. `poetry add langchain-mistralai`).

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the providers you want to use

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a model and a system message. Default key: `sample-completion`.

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
poetry run langchain
```
