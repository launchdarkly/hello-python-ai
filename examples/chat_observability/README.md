# Chat with Observability (Observability Plugin Example)

This example demonstrates how to use the LaunchDarkly observability SDK plugin to monitor AI chat operations. For more details, see the [Python SDK observability reference](https://launchdarkly.com/docs/sdk/observability/python).

The observability plugin automatically captures and sends data to LaunchDarkly:

- **Observability tab**: SDK operations, flag evaluations, error monitoring, logging, and distributed tracing
- **AI Config Monitoring tab**: Token usage, duration, success/error rates, and custom metadata for filtering and analysis

View your data in the LaunchDarkly dashboard under **Observability** tabs.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with an [AI Config](https://launchdarkly.com/docs/home/ai-configs/create) created
- An API key for your AI provider (e.g., OpenAI)

## Setup

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-ai-config
   OPENAI_API_KEY=your-openai-api-key
   ```

   > `LAUNCHDARKLY_AI_CONFIG_KEY` defaults to `sample-ai-config` if not set.

   Optionally, set service identification:

   ```
   SERVICE_NAME=my-ai-service
   SERVICE_VERSION=1.0.0
   ```

2. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run chat-observability-example
```
