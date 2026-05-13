# Create Model Example

This example demonstrates how to use LaunchDarkly's `create_model` method, which handles model creation, chat execution, and optional judge evaluation dispatch automatically.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a model and system message. Default key: `sample-completion`.

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
poetry run model
```
