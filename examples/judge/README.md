# Judge Examples (Judge Evaluation)

These examples demonstrate how to use LaunchDarkly's judge functionality to evaluate AI responses for accuracy, relevance, and other metrics.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A LaunchDarkly account with an [AI Config](https://launchdarkly.com/docs/home/ai-configs/create) created for chat functionality
- A [Judge Config](https://launchdarkly.com/docs/home/ai-configs/judges) created for evaluation
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-ai-config
   LAUNCHDARKLY_AI_JUDGE_KEY=sample-ai-judge-accuracy
   ```

   > `LAUNCHDARKLY_AI_CONFIG_KEY` defaults to `sample-ai-config` if not set.
   > `LAUNCHDARKLY_AI_JUDGE_KEY` defaults to `sample-ai-judge-accuracy` if not set.

   Add the API key for your chosen provider:

   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

2. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

### Chat with automatic judge evaluation

Uses the chat functionality which automatically evaluates responses with any judges defined in the AI config.

```bash
poetry run chat-judge-example
```

### Direct judge evaluation

Evaluates specific input/output pairs using a judge configuration directly.

```bash
poetry run direct-judge-example
```
