# Create Judge Example

This example demonstrates how to use LaunchDarkly's `create_judge` method to evaluate specific input/output pairs directly, without an associated chat session.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create a Judge Config](https://launchdarkly.com/docs/home/ai-configs/judges) for evaluation. Default key: `sample-ai-judge`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_JUDGE_KEY=sample-ai-judge
   OPENAI_API_KEY=your-openai-api-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run judge
```
