# LaunchDarkly AI SDK for Python - Examples

| Package | PyPI | Docs |
| --- | --- | --- |
| [launchdarkly-server-sdk-ai](https://github.com/launchdarkly/python-server-sdk-ai/tree/main/packages/sdk/server-ai) | [![PyPI](https://img.shields.io/pypi/v/launchdarkly-server-sdk-ai)](https://pypi.org/project/launchdarkly-server-sdk-ai/) | [Reference](https://docs.launchdarkly.com/sdk/ai/python) |
| [launchdarkly-server-sdk-ai-openai](https://github.com/launchdarkly/python-server-sdk-ai/tree/main/packages/ai-providers/server-ai-openai) | [![PyPI](https://img.shields.io/pypi/v/launchdarkly-server-sdk-ai-openai)](https://pypi.org/project/launchdarkly-server-sdk-ai-openai/) | [Reference](https://docs.launchdarkly.com/sdk/ai/python) |
| [launchdarkly-server-sdk-ai-langchain](https://github.com/launchdarkly/python-server-sdk-ai/tree/main/packages/ai-providers/server-ai-langchain) | [![PyPI](https://img.shields.io/pypi/v/launchdarkly-server-sdk-ai-langchain)](https://pypi.org/project/launchdarkly-server-sdk-ai-langchain/) | [Reference](https://docs.launchdarkly.com/sdk/ai/python) |
| [launchdarkly-observability](https://github.com/launchdarkly/observability-sdk/tree/main/sdk/%40launchdarkly/observability-python) | [![PyPI](https://img.shields.io/pypi/v/launchdarkly-observability)](https://pypi.org/project/launchdarkly-observability/) | [Reference](https://docs.launchdarkly.com/sdk/observability/python) |

Each example is a self-contained application you can run independently to explore LaunchDarkly's AI APIs hands-on. Pick one that matches your provider or use case, follow the README, and you'll be up and running in minutes.

For more comprehensive instructions, visit the [Quickstart page](https://docs.launchdarkly.com/home/ai-configs/quickstart) or the [Python reference guide](https://docs.launchdarkly.com/sdk/ai/python).

## Getting Started

These examples show how to integrate LaunchDarkly AI with different providers.

| Provider | Example | Description |
| --- | --- | --- |
| Bedrock | [Converse](getting_started/bedrock/converse/) | `completion_config` with AWS Bedrock Converse API, metrics tracking |
| Gemini | [Generate Content](getting_started/gemini/generate_content/) | `completion_config` with Google GenAI, metrics tracking |
| LangChain | [Invoke](getting_started/langchain/invoke/) | `completion_config` with LangChain, async metrics tracking |
| LangGraph | [ReAct Agent](getting_started/langgraph/react_agent/) | `agent_config` with a single LangGraph ReAct agent, tool calling, metrics tracking |
| LangGraph | [StateGraph](getting_started/langgraph/state_graph/) | `agent_config` with multiple LangGraph agents, custom StateGraph workflow, per-node metrics |
| OpenAI | [Chat Completions](getting_started/openai/chat_completions/) | `completion_config` with OpenAI, automatic metrics tracking |

## Features

These examples demonstrate LaunchDarkly's managed APIs and standalone capabilities.

| Example | Description |
| --- | --- |
| [create_judge](features/create_judge/) | Standalone evaluation of AI responses |
| [create_agent](features/create_agent/) | Tool calling, automatic metrics tracking, and judge evaluation |
| [create_agent_graph](features/create_agent_graph/) | Multi-node workflows, tool calling, per-node metrics, and judge evaluation |
| [create_model](features/create_model/) | Managed chat, automatic metrics tracking, and judge evaluation |
