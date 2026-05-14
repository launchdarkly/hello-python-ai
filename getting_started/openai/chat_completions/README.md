# OpenAI Example (Single Provider)

This example demonstrates how to use LaunchDarkly's AI Config with the OpenAI provider.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with an OpenAI model (e.g. `gpt-4`) and a system message. Default key: `sample-completion`.

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
poetry run openai
```
