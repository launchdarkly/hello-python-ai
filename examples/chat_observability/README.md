# Chat with Observability (Observability Plugin Example)

This example demonstrates how to use the LaunchDarkly observability SDK plugin to monitor AI chat operations. For more details, see the [Python SDK observability reference](https://launchdarkly.com/docs/sdk/observability/python).

The observability plugin automatically captures and sends data to LaunchDarkly:

- **Observability tab**: SDK operations, flag evaluations, error monitoring, logging, and distributed tracing
- **AI Config Monitoring tab**: Token usage, duration, success/error rates, and custom metadata for filtering and analysis

View your data in the LaunchDarkly dashboard under **Observability** tabs.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- An API key for your AI provider (e.g., OpenAI)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a model and a system message. Default key: `sample-completion-config`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-completion-config
   OPENAI_API_KEY=your-openai-api-key
   ```

   Optionally, set service identification:

   ```
   SERVICE_NAME=my-ai-service
   SERVICE_VERSION=1.0.0
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run chat
```
