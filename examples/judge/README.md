# Judge Examples (Judge Evaluation)

These examples demonstrate how to use LaunchDarkly's judge functionality to evaluate AI responses for accuracy, relevance, and other metrics.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- API keys for the provider you want to use (OpenAI, Bedrock, or Gemini)

## Setup

1. Create the following configs in your LaunchDarkly project. You can use different keys by setting the environment variables in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a model and system message. Default key: `sample-completion-config`.
   - [Create a Judge Config](https://launchdarkly.com/docs/home/ai-configs/judges) for evaluation. Default key: `sample-ai-judge`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-completion-config
   LAUNCHDARKLY_AI_JUDGE_KEY=sample-ai-judge
   ```

   Add the API key for your chosen provider:

   ```
   OPENAI_API_KEY=your-openai-api-key
   ```

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

### Chat with automatic judge evaluation

Uses the chat functionality which automatically evaluates responses with any judges defined in the AI config.

```bash
poetry run chat-judge
```

### Direct judge evaluation

Evaluates specific input/output pairs using a judge configuration directly.

```bash
poetry run direct-judge
```
