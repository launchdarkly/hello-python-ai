# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://app.launchdarkly.com/quickstart#/) or the [Python reference guide](https://docs.launchdarkly.com/sdk/server-side/python).

This demo requires Python 3.8 or higher.

## Build Instructions

This repository includes examples for `OpenAI` and `Bedrock`.

1. Set the environment variable `LAUNCHDARKLY_SDK_KEY` to your LaunchDarkly SDK key. If there is an existing an AI Config in your LaunchDarkly project that you want to evaluate, set `LAUNCHDARKLY_AI_CONFIG_KEY` to the flag key; otherwise, an AI Config of `sample-ai-config` will be assumed.

   ```bash
   export LAUNCHDARKLY_SDK_KEY="1234567890abcdef"
   export LAUNCHDARKLY_AI_CONFIG_KEY="sample-ai-config"
   ```

1. Ensure you have [Poetry](https://python-poetry.org/) installed.
1. Install the required dependencies with `poetry install --all-extras`. Alternatively, you can install with `poetry install -E open` or `poetry install -E bedrock` to opt into only those required dependencies.
1. On the command line, run `openai-example` or `bedrock-example` as relevant.

You should receive an output of the model configuration and prompt being sent to the chosen provider.
