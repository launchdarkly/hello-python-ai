# LangChain Example (Multiple Providers)

This example demonstrates how to use LaunchDarkly's AI Config with LangChain, supporting multiple providers including OpenAI, Bedrock, and Gemini. You can add additional LangChain providers using the `poetry add` command.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the providers you want to use

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a model and a system message. Default key: `sample-completion-config`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-completion-config
   ```

   Add the API keys for the providers you want to use:

   ```
   OPENAI_API_KEY=your-openai-api-key
   GOOGLE_API_KEY=your-google-api-key
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run langchain-example
```
