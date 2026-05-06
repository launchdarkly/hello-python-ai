# Gemini Example (Single Provider)

This example demonstrates how to use LaunchDarkly's AI Config with the Google Gemini provider.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- A [Google API key](https://aistudio.google.com/apikey)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a Gemini model (e.g. `gemini-2.0-flash`) and a system message. Default key: `sample-completion-config`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-completion-config
   GOOGLE_API_KEY=your-google-api-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run gemini-example
```
