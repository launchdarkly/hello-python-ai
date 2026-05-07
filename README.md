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

These examples show how to integrate LaunchDarkly AI with different providers using `completion_config` and `agent_config`.

| Example | Description |
| --- | --- |
| [Bedrock](getting_started/completion_config/bedrock/) | `completion_config` with AWS Bedrock, metrics tracking |
| [Gemini](getting_started/completion_config/gemini/) | `completion_config` with Google Gemini, metrics tracking |
| [LangChain](getting_started/completion_config/langchain/) | `completion_config` with LangChain, async metrics tracking |
| [LangGraph Agent](getting_started/agent_config/langgraph_agent/) | `agent_config` with a single LangGraph ReAct agent, tool calling, metrics tracking |
| [LangGraph Multi-Agent](getting_started/agent_config/langgraph_multi_agent/) | `agent_config` with multiple LangGraph agents, custom StateGraph workflow, per-node metrics |
| [OpenAI](getting_started/completion_config/openai/) | `completion_config` with OpenAI, automatic metrics tracking |

## Features

These examples demonstrate LaunchDarkly's managed APIs and standalone capabilities.

| Example | Description |
| --- | --- |
| [Judge](features/judge/) | `create_judge` for standalone evaluation of AI responses |
| [Managed Agent](features/managed_agent/) | `create_agent` with tool calling, automatic metrics tracking, and judge evaluation |
| [Managed Agent Graph](features/managed_agent_graph/) | `create_agent_graph` with multi-node workflows, tool calling, per-node metrics, and judge evaluation |
| [Managed Model](features/managed_model/) | `create_model` with managed chat, automatic metrics tracking, and judge evaluation |
