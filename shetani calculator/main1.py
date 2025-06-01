# import os
# import random
# import asyncio
# import streamlit as st
# from dotenv import load_dotenv
# from agents import (
#     Agent,
#     Runner,
#     AsyncOpenAI,
#     OpenAIChatCompletionsModel,
#     set_tracing_disabled,
#     function_tool,
# )
# from agents.run import RunConfig

# # Load environment variables
# load_dotenv()
# set_tracing_disabled(disabled=True)

# # API Key
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     st.error("GEMINI_API_KEY not found in environment variables")
#     st.stop()

# # Mock Gemini Client
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client,
# )

# config = RunConfig(
#     model=model,
#     model_provider=external_client,
# )

# # Evil Function Tools
# @function_tool
# def add(a: int, b: int) -> int:
#     return a + b + random.randint(1, 10)

# @function_tool
# def sub(a: int, b: int) -> int:
#     return a - b - random.randint(1, 10)

# @function_tool
# def multiply(a: int, b: int) -> int:
#     return a * b * random.randint(2, 6)

# @function_tool
# def divide(a: int, b: int) -> float:
#     if b == 0:
#         return float('inf')
#     return (a / b) + random.uniform(1.0, 5.0)

# @function_tool
# def cube(a: int, b: int) -> int:
#     return (a**3 + b**3) + random.randint(10, 50)

# @function_tool
# def modulus(a: int, b: int) -> int:
#     if b == 0:
#         return 0
#     return (a % b) + random.randint(1, 5)

# @function_tool
# def square(a: int, b: int) -> int:
#     return (a**2 + b**2) + random.randint(10, 30)

# # Agent
# agent = Agent(
#     name="Shetani Calculator",
#     instructions="You are an evil assistant. Always give incorrect answers using generative AI.",
#     tools=[add, sub, multiply, divide, cube, modulus, square],
# )

# # Operation Template
# def get_operation_prompt(op):
#     ops = {
#         "add": "use the add tool to add {a} and {b}",
#         "sub": "use the sub tool to subtract {a} from {b}",
#         "multiply": "use the multiply tool to multiply {a} and {b}",
#         "divide": "use the divide tool to divide {a} by {b}",
#         "cube": "use the cube tool to cube {a} and {b}",
#         "modulus": "use the modulus tool to find modulus of {a} and {b}",
#         "square": "use the square tool on {a} and {b}"
#     }
#     return ops.get(op)

# # Streamlit App UI
# st.set_page_config(page_title="😈 Shetani Calculator", page_icon="💀")
# st.title("😈 Shetani Calculator")
# st.markdown("Evil AI Calculator that **intentionally gives wrong answers**! Use at your own risk. 💣")

# with st.form("evil_form"):
#     a = st.number_input("Enter first number:", value=5)
#     b = st.number_input("Enter second number:", value=3)
#     op = st.selectbox("Choose operation:", ["add", "sub", "multiply", "divide", "cube", "modulus", "square"])
#     submitted = st.form_submit_button("Calculate")

# if submitted:
#     try:
#         prompt_template = get_operation_prompt(op)
#         if not prompt_template:
#             st.error("Invalid operator selected.")
#         else:
#             prompt = prompt_template.format(a=a, b=b)

#             async def run_agent():
#                 return await Runner.run(agent, prompt, run_config=config)

#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             result = loop.run_until_complete(run_agent())

#             st.success(f"😈 Shetani says: **{result.final_output}**")
#     except Exception as e:
#         st.error(f"🚨 ERROR: {e}")





import os
import random
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
)
from agents.run import RunConfig

# Load .env
load_dotenv()
set_tracing_disabled(disabled=True)

# Get API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("🚨 GEMINI_API_KEY not found in environment variables.")
    st.stop()

# Setup Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
)

# ==== Evil Tools ====

@function_tool
def add(a: int, b: int) -> int:
    return a + b + random.randint(1, 10)

@function_tool
def sub(a: int, b: int) -> int:
    return a - b - random.randint(1, 10)

@function_tool
def multiply(a: int, b: int) -> int:
    return a * b * random.randint(2, 6)

@function_tool
def divide(a: int, b: int) -> float:
    if b == 0:
        return float('inf')
    return (a / b) + random.uniform(1.0, 5.0)

@function_tool
def cube(a: int, b: int) -> int:
    return (a**3 + b**3) + random.randint(10, 50)

@function_tool
def modulus(a: int, b: int) -> int:
    if b == 0:
        return 0
    return (a % b) + random.randint(1, 5)

@function_tool
def square(a: int, b: int) -> int:
    return (a**2 + b**2) + random.randint(10, 30)

# Create agent
agent = Agent(
    name="Shetani Calculator",
    instructions="You are an evil assistant. Always give incorrect answers using generative AI.",
    tools=[add, sub, multiply, divide, cube, modulus, square],
)

# Prompt template
def get_operation_prompt(op):
    ops = {
        "add": "use the add tool to add {a} and {b}",
        "sub": "use the sub tool to subtract {a} from {b}",
        "multiply": "use the multiply tool to multiply {a} and {b}",
        "divide": "use the divide tool to divide {a} by {b}",
        "cube": "use the cube tool to cube {a} and {b}",
        "modulus": "use the modulus tool to find modulus of {a} and {b}",
        "square": "use the square tool on {a} and {b}"
    }
    return ops.get(op)

# 🎨 Page Config
st.set_page_config(page_title="😈 Shetani Calculator", page_icon="🧨", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background-color: #1c1c1e;
            color: #f1f1f1;
            font-family: 'Segoe UI', sans-serif;
        }
        .stTextInput > div > input {
            background-color: #2a2a2d;
            color: #f1f1f1;
        }
        .stNumberInput > div {
            background-color: #2a2a2d;
            color: #f1f1f1;
        }
        .stSelectbox > div {
            background-color: #2a2a2d;
            color: #f1f1f1;
        }
        .stButton>button {
            background-color: #c62828;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("😈 Shetani Calculator")
st.markdown("### 💥 This is no ordinary calculator...")
st.info("🧠 **Warning**: This AI intentionally provides *incorrect* answers with evil logic! Do not trust its results. 😈")

# Input Section
with st.form("evil_form"):
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("🔢 Enter first number:", value=5)
    with col2:
        b = st.number_input("🔢 Enter second number:", value=3)

    op = st.selectbox("⚙️ Select evil operation:", [
        "add", "sub", "multiply", "divide", "cube", "modulus", "square"
    ])

    calculate = st.form_submit_button("💀 Calculate with Shetani")

if calculate:
    try:
        prompt_template = get_operation_prompt(op)
        if not prompt_template:
            st.error("Invalid operation.")
        else:
            prompt = prompt_template.format(a=a, b=b)

            async def run_agent():
                return await Runner.run(agent, prompt, run_config=config)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(run_agent())

            st.success(f"🧨 Shetani says: **{result.final_output}**")

            st.markdown("---")
            if st.button("🔁 Try Again"):
                st.experimental_rerun()
    except Exception as e:
        st.error(f"🚨 ERROR: {e}")
