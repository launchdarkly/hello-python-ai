import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai.client import LDAIClient, AIConfig, ModelConfig, ProviderConfig, LDMessage
from google import genai
from google.genai import types
from typing import List, Optional, Tuple

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

# Set Google API key
google_api_key = os.getenv('GOOGLE_API_KEY')

def map_to_google_ai_messages(
    input_messages: List[LDMessage]
) -> Tuple[Optional[str], List[types.Content]]:
    messages: List[types.Content] = []

    system_messages: List[str] = []
    
    for message in input_messages:
        if message.role == 'system':
            system_messages.append(message.content)
            continue
        elif message.role == 'assistant':
            role = "model"
            parts = [types.Part(text=message.content)]
        elif message.role == 'user':
            role = "user"
            parts = [types.Part(text=message.content)]
        else:
            # Skip other message types
            continue

        messages.append(types.Content(role=role, parts=parts))
    
    # Concatenate system messages with spaces
    system_instruction = " ".join(system_messages) if system_messages else None
    return system_instruction, messages


def main():
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not ai_config_key:
        print("*** Please set the LAUNCHDARKLY_AI_CONFIG_KEY env first")
        exit()
    if not google_api_key:
        print("*** Please set the GOOGLE_API_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    aiclient = LDAIClient(ldclient.get())

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = (
        Context
        .builder('example-user-key')
        .kind('user')
        .name('Sandy')
        .build()
    )

    DEFAULT_SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks."

    # Set a fallback AIConfig to use if a config is not found or your application is not able to connect to LaunchDarkly.
    default_value = AIConfig(
        enabled=True,
        model=ModelConfig(name='gemini-pro', parameters={}),
        provider=ProviderConfig(name='google'),
        messages=[LDMessage(role='system', content=DEFAULT_SYSTEM_MESSAGE)],
    )

    # Optionally, you can use a disabled AIConfig
    # default_value = AIConfig(
    #     enabled=False
    # )

    config_value, tracker = aiclient.config(
        ai_config_key,
        context,
        default_value,
        {'myUserVariable': "Testing Variable"}
    )

    if not config_value.enabled:
        print("AI Config is disabled")
        return

    # Configure Google Generative AI
    client = genai.Client(
        api_key=google_api_key,
    )

    # Convert LaunchDarkly messages to Google AI format using the helper function
    system_instruction, messages = map_to_google_ai_messages(config_value.messages or [])
    
    # Add the user input to the conversation
    USER_INPUT = "What can you help me with?"
    print("User Input:\n", USER_INPUT)
    user_message = types.Content(role="user", parts=[types.Part(text=USER_INPUT)])
    messages.append(user_message)

    completion = tracker.track_openai_metrics(lambda: client.models.generate_content(
        model=config_value.model.name,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
        )
    ))
    ai_response = completion.text

    # Add the AI response to the conversation history
    ai_message = types.Content(role="model", parts=[types.Part(text=ai_response)])
    messages.append(ai_message)
    print("AI Response:\n", ai_response)

    # Continue the conversation by adding user input to the messages list and invoking the LLM again.
    print("Success.")

    # Close the client to flush events and close the connection.
    ldclient.get().close()

if __name__ == "__main__":
    main() 
