# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://app.launchdarkly.com/quickstart#/) or the [Python reference guide](https://docs.launchdarkly.com/sdk/server-side/python).

This demo requires Python 3.8 or higher.

## Build instructions

1. Set the environment variable `LAUNCHDARKLY_SDK_KEY` to your LaunchDarkly SDK key. If there is an existing boolean feature flag in your LaunchDarkly project that you want to evaluate, set `LAUNCHDARKLY_AI_CONFIG_KEY` to the flag key; otherwise, a boolean flag of `sample-ai-config` will be assumed.

   ```bash
   export LAUNCHDARKLY_SDK_KEY="1234567890abcdef"
   export LAUNCHDARKLY_AI_CONFIG_KEY="sample-ai-config"
   ```

2. Ensure you have [Poetry](https://python-poetry.org/) installed.
3. Install the required dependencies with `poetry install`.
4. On the command line, run `poetry run python main.py`

You should receive an output of the model configuration and prompt being sent to Bedrock.
