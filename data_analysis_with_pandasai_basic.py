from pandasai import SmartDataframe
from pandasai import Agent
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM
import os
import pandas as pd

# Initialize PandasAI with OpenAI (using OpenRouter)
llm = LiteLLM(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openrouter/mistralai/mistral-7b-instruct:free"
    #,base_url="https://openrouter.ai/api/v1"
)

pai.config.set({"llm": llm})

# Load the CSV file
df = pd.DataFrame(
    {
        'employee': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'department': ['Sales', 'IT', 'Sales', 'Sales'],
        'salary': [5000, 3200, 2900, 4100]
    }
)

agent = Agent(df)
response = agent.chat("What is average salary?")

print(response)