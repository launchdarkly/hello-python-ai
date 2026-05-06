# OpenAI Example (Single Provider)

This example demonstrates how to use LaunchDarkly's AI Config with the OpenAI provider.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with an OpenAI model (e.g. `gpt-4`) and a system message. Default key: `sample-completion-config`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-completion-config
   OPENAI_API_KEY=your-openai-api-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run openai-example
```
