import asyncio
from openai import AsyncOpenAI
from agents import Agent,OpenAIChatCompletionsModel,Runner,set_tracing_disabled
from dotenv import load_dotenv
import os 

load_dotenv()

OPENROUTER_API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure you have set this in your .env file
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL = "gemini-2.0-flash"

client = AsyncOpenAI(api_key = OPENROUTER_API_KEY, base_url = BASE_URL)
set_tracing_disabled(disabled=True)


async def main():
    agent = Agent(
        name = "RSK BOT",
        instructions = "You are a helpful assistant that can answer questions and help with tasks.",
        model = OpenAIChatCompletionsModel(model = MODEL, openai_client = client),
    )
    
    print("🤖 RSK BOT is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("You:")
        if user_input.lower() in {"exit", "quit"}:
            break

        result = await Runner.run(agent, user_input)
        print("Assistant:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())