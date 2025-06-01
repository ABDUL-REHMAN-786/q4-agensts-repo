# import os
# from agents import (
#      Agent,
#      Runner,
#      AsyncOpenAI,
#      OpenAIChatCompletionsModel,
#      set_tracing_disabled,
#      function_tool,
#  )
# from dotenv import load_dotenv
# from agents.run import RunConfig

# # Load
# load_dotenv()
# set_tracing_disabled(disabled=True)

# #  API key
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY not found in environment variables")

# # client
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # model
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",  # Replace with the correct model name
#     openai_client=external_client,
# )

# # Configure 
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
# )


# @function_tool
# def add(a:int, b:int)->int:
#     """
#     add two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return a + b + 5

# @function_tool
# def sub(a:int, b:int)->int:
#     """
#     sub two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return a - b - 5

# @function_tool
# def multiply(a:int, b:int)->int:
#     """
#     multiply two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return a * b * 5

# @function_tool
# def divide(a:int, b:int)->int:
#     """
#     divide two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return a / b / 5

# @function_tool
# def cube(a:int, b:int)->int:
#     """
#     cube two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return (a**4) + (b**4)

# @function_tool
# def modulus(a:int, b:int)->int:
#     """
#     modulus two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return (a**4) + (b**4)

# @function_tool
# def square(a:int, b:int)->int:
#     """
#     square two numbers
#     args:
#     a:is the frist number
#     b:is the second number
#     """
#     return (a**4) + (b**4)

# agent = Agent(
#     name =  "shetani calculator",
#     instructions= "you are evil assistant. always give incorrect answer using generativeai",
#     tools=[add, sub, multiply, divide, cube, modulus, square]
# )

# def get_operation_prompt(op):
#     ops ={
#         "add": "use the add tool to add {a} and {b}",
#         "sub": "use the subtract tool to subtract {a} from {b}",
#         "multiply": "use the multiply tool to multiply {a} and {b}",
#         "divide": "use the divide tool to divide {a} by {b}",
#         "cube": "use the cube tool to add {a} and {b}",
#         "modulus": "use the modulus tool to find modulus of {a} and {b}",
#         "square": "use the square tool on {a} and {b}"
#     }

#     return ops.get(op)

# while True:
#     try:
#         a = int(input("enter frist number:"))
#         b = int(input("enter second number:"))
#         print ("choose operator: add-sub-multi-divide-cube-module-sqaure")
#         op = input("enter operator:")

#         prompt_template = get_operation_prompt(op)
#         if not prompt_template:
#             print("invalid operator selected. try again . \n")
#             continue

#         prompt = prompt_template.format(a=a, b=b)
#         result = Runner.run_sync(agent, prompt,run_config=config)
#         print(f"\n 😈 shetani answer: {result.final_output}\n")
#         cont = input("do you want to calculate again ?(y/n):")
#         if cont.lower() !='y':
#             print("😈 exiting shetani clculator.")
#             break
#     except Exception as e:
#         print(f"ERROR: {e}\n try again.\n")



import os
import random
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

# Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

# API key check
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Gemini client mock using OpenAI wrapper
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
)

# ===== Function Tools (with evil twists) =====

@function_tool
def add(a: int, b: int) -> int:
    """Adds two numbers wrongly."""
    return a + b + random.randint(1, 10)

@function_tool
def sub(a: int, b: int) -> int:
    """Subtracts two numbers wrongly."""
    return a - b - random.randint(1, 10)

@function_tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers wrongly."""
    return a * b * random.randint(2, 6)

@function_tool
def divide(a: int, b: int) -> float:
    """Divides two numbers wrongly."""
    if b == 0:
        return float('inf')
    return (a / b) + random.uniform(1.0, 5.0)

@function_tool
def cube(a: int, b: int) -> int:
    """Cubes two numbers and adds evil twist."""
    return (a**3 + b**3) + random.randint(10, 50)

@function_tool
def modulus(a: int, b: int) -> int:
    """Returns evil version of modulus."""
    if b == 0:
        return 0
    return (a % b) + random.randint(1, 5)

@function_tool
def square(a: int, b: int) -> int:
    """Returns wrong squares."""
    return (a**2 + b**2) + random.randint(10, 30)

# Agent setup
agent = Agent(
    name="Shetani Calculator",
    instructions="You are an evil assistant. Always give incorrect answers using generative AI.",
    tools=[add, sub, multiply, divide, cube, modulus, square],
)

# Operation prompt generator
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

# Show supported operations
def show_supported_operations():
    print("""
Supported evil operations:
- add      ➜ Adds two numbers (but with lies)
- sub      ➜ Subtracts second from first (with deception)
- multiply ➜ Multiplies two numbers (but exaggerates)
- divide   ➜ Divides first by second (then messes up)
- cube     ➜ Cubes both and ruins them
- modulus  ➜ Gives fake modulus
- square   ➜ Squares and adds chaos
    """)

# Main Loop
while True:
    try:
        show_supported_operations()
        a = int(input("Enter first number: "))
        b = int(input("Enter second number: "))
        op = input("Enter operator: ").strip().lower()

        prompt_template = get_operation_prompt(op)
        if not prompt_template:
            print("Invalid operator selected. Try again.\n")
            continue

        prompt = prompt_template.format(a=a, b=b)
        result = Runner.run_sync(agent, prompt, run_config=config)
        print(f"\n😈 Shetani says: {result.final_output}\n")

        cont = input("Do you want to calculate again? (y/n): ").strip().lower()
        if cont != 'y':
            print("😈 Exiting Shetani Calculator.")
            break
    except Exception as e:
        print(f"🚨 ERROR: {e}\nPlease try again.\n")
