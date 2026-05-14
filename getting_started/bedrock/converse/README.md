# Bedrock Example (Single Provider)

This example demonstrates how to use LaunchDarkly's AI Config with the AWS Bedrock provider.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- AWS credentials configured for Bedrock access

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a Bedrock model and a system message. Default key: `sample-completion`.

1. Copy `.env.example` to `.env` and fill in your keys:

   ```bash
   cp .env.example .env
   ```

   `LAUNCHDARKLY_COMPLETION_KEY` defaults to `sample-completion` if not set.

   Ensure your AWS credentials can be [auto-detected by the `boto3` library](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html). Setting them in `.env` is one option; role providers or shared credential files are also supported.

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run bedrock
```
