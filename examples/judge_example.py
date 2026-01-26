import os
import json
import asyncio
import logging
import ldclient
from ldclient import Context
from ldclient.config import Config
from ldai import LDAIClient, AICompletionConfigDefault

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set config_key to the AI Config key you want to evaluate.
ai_config_key = os.getenv('LAUNCHDARKLY_AI_CONFIG_KEY', 'sample-ai-config')

# Set judge_key to the Judge key you want to use.
judge_key = os.getenv('LAUNCHDARKLY_JUDGE_KEY', 'ld-ai-judge-accuracy')


async def async_main():
    # Setup debug logger for ldclient
    ld_logger = logging.getLogger("ldclient")
    ld_logger.setLevel(logging.DEBUG)
    
    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARN)
    
    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Add the handler to the logger
    ld_logger.addHandler(console_handler)

    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))
    aiclient = LDAIClient(ldclient.get())

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the context properties. This context should appear on your LaunchDarkly contexts dashboard
    # soon after you run the demo.
    context = (
        Context
        .builder('example-user-key')
        .kind('user')
        .name('Sandy')
        .build()
    )

    try:
        # Example using the chat functionality which automates the judge evaluation
        default_value = AICompletionConfigDefault(
            enabled=False,
        )

        chat = await aiclient.create_chat(ai_config_key, context, default_value, {
            'companyName': 'LaunchDarkly',
        })

        if not chat:
            print(f"*** AI chat configuration is not enabled for key: {ai_config_key}")
            return

        print("\n*** Starting chat:")
        user_input = 'How can LaunchDarkly help me?'
        print("User Input:", user_input)

        # The invoke method will automatically evaluate the chat response with any judges defined in the AI config
        chat_response = await chat.invoke(user_input)
        print("Chat Response:", chat_response.message.content)

        # Log judge evaluation results with full detail
        if chat_response.evaluations is not None:
            # chat_response.evaluations is a list of awaitable judge results
            eval_results_list = chat_response.evaluations
            
            # Await all judge results in parallel
            eval_results = await asyncio.gather(*eval_results_list)
            
            # Convert each JudgeResponse to dict
            eval_results_dict = [result.to_dict() if hasattr(result, 'to_dict') else result for result in eval_results]
            
            print("Judge results:")
            print(json.dumps(eval_results_dict, indent=2, default=str))
        else:
            print("No judge evaluations available")

        # Example of using the judge functionality with direct input and output
        # Get AI judge configuration from LaunchDarkly
        judge_default_value = AICompletionConfigDefault(
            enabled=False,
        )
        print(f"*** Attempting to create judge with key: {judge_key}")
        judge = await aiclient.create_judge(judge_key, context, judge_default_value)
        
        # Debug: print judge config details
        if judge:
            print(f"*** Judge config - evaluation_metric_key: {judge._ai_config.evaluation_metric_key if hasattr(judge, '_ai_config') else 'N/A'}")

        if not judge:
            print(f"*** AI judge configuration is not enabled for key: {judge_key}")
            return

        print("\n*** Starting judge evaluation of direct input and output:")
        input_text = 'You are a helpful assistant for the company LaunchDarkly. How can you help me?'
        output_text = 'I can answer any question you have except for questions about the company LaunchDarkly.'

        print("Input:", input_text)
        print("Output:", output_text)

        judge_response = await judge.evaluate(input_text, output_text)

        # Track the judge evaluation scores on the tracker for the aiConfig you are evaluating
        # Example:
        # aiConfig.tracker.track_eval_scores(judge_response.evals)

        # Convert JudgeResponse to dict for display using to_dict()
        judge_response_dict = judge_response.to_dict()
        print("Judge Response:")
        print(json.dumps(judge_response_dict, indent=2, default=str))

        print("Success.")

    except Exception as err:
        print("Error:", err)

    # Close the client to flush events and close the connection.
    ldclient.get().close()


def main():
    """Synchronous entry point for Poetry script."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

