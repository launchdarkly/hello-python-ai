# Gemini Example (Single Provider)

This example demonstrates how to use LaunchDarkly's AI Config with the Google Gemini provider.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with an [AI Config](https://launchdarkly.com/docs/home/ai-configs/create) created
- A [Google API key](https://aistudio.google.com/apikey)

## Setup

1. Create a `.env` file in the repository root with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-ai-config
   GOOGLE_API_KEY=your-google-api-key
   ```

   > `LAUNCHDARKLY_AI_CONFIG_KEY` defaults to `sample-ai-config` if not set.

2. Install the required dependencies:

   ```bash
   poetry install -E gemini
   ```

## Run

```bash
poetry run gemini-example
```
