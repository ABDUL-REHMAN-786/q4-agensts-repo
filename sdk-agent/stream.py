# import streamlit as st
# from dotenv import load_dotenv
# import os
# import asyncio

# from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
# from agents.run import RunConfig

# # Load environment variables
# load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     st.error("GEMINI_API_KEY environment variable is not set.")
#     st.stop()

# # Provider and model setup
# provider = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai",
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-1.5-flash",
#     openai_client=provider
# )

# config = RunConfig(
#     model=model,
#     model_provider=provider,
#     tracing_disabled=True
# )

# # Tools
# @function_tool
# def get_capital_of_country(country: str) -> str:
#     capitals = {
#         "France": "Paris",
#         "Germany": "Berlin",
#         "Italy": "Rome",
#         "Spain": "Madrid"
#     }
#     return capitals.get(country, "Unknown")

# @function_tool
# def get_population_of_country(country: str) -> int:
#     populations = {
#         "France": 65273511,
#         "Germany": 83783942,
#         "Italy": 60244639,
#         "Spain": 46754778
#     }
#     return populations.get(country, 0)

# # Agent setup
# agent = Agent(
#     name="AI Assistant",
#     instructions="You are a helpful AI assistant.",
#     model=model,
#     tools=[get_capital_of_country, get_population_of_country]
# )

# # Utility to run async function in sync environment (fixes event loop error)
# def run_async(func, *args, **kwargs):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#     if loop.is_running():
#         return asyncio.create_task(func(*args, **kwargs))
#     else:
#         return loop.run_until_complete(func(*args, **kwargs))

# # Streamlit UI
# st.set_page_config(page_title="AI Assistant", page_icon="🤖")
# st.title("🤖 AI Assistant")
# st.markdown("Ask anything about country capitals or populations!")

# # Session state
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Input area
# with st.form("user_input_form"):
#     user_input = st.text_input("💬 Your question", "")
#     submitted = st.form_submit_button("Ask")

# if submitted and user_input:
#     try:
#         with st.spinner("🤖 Thinking..."):
#             result = run_async(Runner.run, agent, user_input, run_config=config)
#             if asyncio.iscoroutine(result):
#                 result = asyncio.run(result)

#         st.session_state.chat_history.append(("You", user_input))
#         st.session_state.chat_history.append(("Assistant", result.final_output))
#     except Exception as e:
#         st.error(f"❌ Error: {e}")

# # Display chat history
# for sender, message in st.session_state.chat_history:
#     with st.chat_message(sender):
#         st.write(message)

# # Sidebar tools
# st.sidebar.title("🛠 Tools & Options")

# if st.sidebar.button("Show Available Tools"):
#     st.sidebar.info("""🔧 Tools:
# - get_capital_of_country(country: str)
# - get_population_of_country(country: str)
# """)

# if st.sidebar.button("Show Help / Instructions"):
#     st.sidebar.success("""
# 💡 Example Questions:
# - What is the capital of Germany?
# - What is the population of France?

# Use the input box above and press 'Ask'.
# """)

# if st.sidebar.button("🧹 Clear Chat"):
#     st.session_state.chat_history = []
#     st.rerun()



import streamlit as st
from dotenv import load_dotenv
import os
import asyncio
import requests

from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
from agents.run import RunConfig

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    st.error("GEMINI_API_KEY environment variable is not set.")
    st.stop()

# Provider and model setup
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=provider
)

config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)

# Dynamic tool using REST Countries API
@function_tool
def get_country_info(country: str) -> dict:
    """Get dynamic information about a country including capital, population, region, subregion, currency, and languages."""
    url = f"https://restcountries.com/v3.1/name/{country}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Country '{country}' not found."}

    data = response.json()[0]

    capital = data.get("capital", ["Unknown"])[0]
    population = data.get("population", 0)
    region = data.get("region", "Unknown")
    subregion = data.get("subregion", "Unknown")

    currencies = ", ".join([v["name"] for v in data.get("currencies", {}).values()]) or "Unknown"
    languages = ", ".join(data.get("languages", {}).values()) or "Unknown"

    return {
        "capital": capital,
        "population": population,
        "region": region,
        "subregion": subregion,
        "currencies": currencies,
        "languages": languages
    }

# Agent setup
agent = Agent(
    name="CountryBot",
    instructions="You are a helpful assistant that answers questions about countries using tools.",
    model=model,
    tools=[get_country_info]
)

# Utility to run async in sync context
def run_async(func, *args, **kwargs):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if loop.is_running():
        return asyncio.create_task(func(*args, **kwargs))
    else:
        return loop.run_until_complete(func(*args, **kwargs))

# Streamlit UI
st.set_page_config(page_title="🌍 AI Country Assistant", page_icon="🌍")
st.title("🌍 AI Country Assistant")
st.markdown("Ask anything about countries: capital, population, languages, etc.")

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input area
with st.form("user_input_form"):
    user_input = st.text_input("💬 Your question", "")
    submitted = st.form_submit_button("Ask")

if submitted and user_input:
    try:
        with st.spinner("🤖 Thinking..."):
            result = run_async(Runner.run, agent, user_input, run_config=config)
            if asyncio.iscoroutine(result):
                result = asyncio.run(result)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", result.final_output))
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Display chat history
for sender, message in st.session_state.chat_history:
    with st.chat_message(sender):
        st.write(message)

# Sidebar tools
st.sidebar.title("🛠 Options & Tools")

if st.sidebar.button("Show Tool Info"):
    st.sidebar.info("""
🔧 Tool Available:
- `get_country_info(country: str)`  
Returns capital, population, region, subregion, currencies, and languages.
""")

if st.sidebar.button("Show Help / Examples"):
    st.sidebar.success("""
💬 Try asking:
- What is the capital of Brazil?
- How many people live in India?
- What language is spoken in Japan?
- Tell me about Canada.
""")

if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
