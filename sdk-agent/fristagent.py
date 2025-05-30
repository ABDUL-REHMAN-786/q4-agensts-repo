from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is set; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
# Print the API key for debugging purposes (optional)
if gemini_api_key:
    print("GEMINI_API_KEY is set.")
print(gemini_api_key)
# Create an instance of AsyncOpenAI with the Gemini API key and base URL


#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Write Agent
fristagent = Agent(
    name = 'Writer Agent',
    instructions= 

    """You are a frist-agent."""
)

# Run the agent with the provided input and configuration
response = Runner.run_sync(
    fristagent,
    input = 'Write a sdk detail notes and agents notes and roadmap heading and sub heading with color full text on Generative AI..',
    run_config = config
    )

# Print the final output of the agent's response
print(response.final_output)