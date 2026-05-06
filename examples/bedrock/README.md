# Bedrock Example (Single Provider)

This example demonstrates how to use LaunchDarkly's AI Config with the AWS Bedrock provider.

## Prerequisites

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/) installed
- A [LaunchDarkly](https://launchdarkly.com/) account and SDK key
- AWS credentials configured for Bedrock access

## Setup

1. Create the following config in your LaunchDarkly project. You can use a different key by setting the environment variable in your `.env`.

   - [Create an AI Config](https://launchdarkly.com/docs/home/ai-configs/create) with a Bedrock model and a system message. Default key: `sample-completion-config`.

1. Create a `.env` file in this directory with the following variables:

   ```
   LAUNCHDARKLY_SDK_KEY=your-launchdarkly-sdk-key
   LAUNCHDARKLY_AI_CONFIG_KEY=sample-completion-config
   ```

   > `LAUNCHDARKLY_AI_CONFIG_KEY` defaults to `sample-completion-config` if not set.

1. Ensure your AWS credentials can be [auto-detected by the `boto3` library](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html). You can set them in your `.env` file:

   ```
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   AWS_DEFAULT_REGION=us-east-1
   ```

   Other options include role providers or shared credential files.

1. Install the required dependencies:

   ```bash
   poetry install
   ```

## Run

```bash
poetry run bedrock-example
```
