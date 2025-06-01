import os
import random
import streamlit as st
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
    function_tool,
)
from dotenv import load_dotenv
from agents.run import RunConfig

# Load .env
load_dotenv()
set_tracing_disabled(disabled=True)

# API setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("🚨 GEMINI_API_KEY not found in environment variables.")
    st.stop()

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

config = RunConfig(
    model=model,
    model_provider=external_client,
)

# Evil function tools
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

# Shetani Agent
agent = Agent(
    name="Shetani Calculator",
    instructions="You are an evil assistant. Always give incorrect answers using generative AI.",
    tools=[add, sub, multiply, divide, cube, modulus, square],
)

# Prompt template
def get_operation_prompt(op):
    prompts = {
        "add": "use the add tool to add {a} and {b}",
        "sub": "use the sub tool to subtract {a} from {b}",
        "multiply": "use the multiply tool to multiply {a} and {b}",
        "divide": "use the divide tool to divide {a} by {b}",
        "cube": "use the cube tool to cube {a} and {b}",
        "modulus": "use the modulus tool to find modulus of {a} and {b}",
        "square": "use the square tool on {a} and {b}"
    }
    return prompts.get(op)

# Streamlit UI
st.set_page_config(page_title="😈 Shetani Calculator", layout="centered", initial_sidebar_state="collapsed")

st.markdown("<h1 style='text-align: center; color: red;'>😈 Shetani Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Get hilariously wrong answers from your favorite evil AI.</p>", unsafe_allow_html=True)

with st.form("shetani_form"):
    a = st.number_input("Enter first number", value=0)
    b = st.number_input("Enter second number", value=0)
    operation = st.selectbox("Choose operation", ["add", "sub", "multiply", "divide", "cube", "modulus", "square"])
    submitted = st.form_submit_button("👿 Calculate")

if submitted:
    prompt_template = get_operation_prompt(operation)
    if not prompt_template:
        st.error("Invalid operation selected.")
    else:
        prompt = prompt_template.format(a=a, b=b)
        with st.spinner("Contacting dark forces..."):
            try:
                result = Runner.run_sync(agent, prompt, run_config=config)
                st.success("Done!")
                st.markdown(f"<h3>😈 Shetani says: {result.final_output}</h3>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
