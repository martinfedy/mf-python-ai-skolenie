## Analyze data with OpenAI

The script reads the CSV file at `users_data.csv`, counts the data rows   
(excluding the header), and loads the full CSV text into a single natural-language prompt   
requesting a basic data analysis. It initializes an OpenAI client, constructs the prompt  
(asking for dataset structure, basic statistics, patterns, data-quality observations,  
and recommendations), then sends that prompt to the Responses API and captures the model's reply. 

```python
from openai import OpenAI
import csv

client = OpenAI()

# Read CSV file
csv_file_path = "data/users_data.csv"

# Read CSV data
with open(csv_file_path, 'r') as file:
    csv_content = file.read()

# Count rows for context
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    row_count = sum(1 for row in csv_reader) - 1  # Subtract header row

# Prepare prompt for LLM
prompt = f"""Please analyze the following CSV dataset containing {row_count} user records.

CSV Data:
{csv_content}

Please provide:
1. A summary of the dataset structure and key columns
2. Basic statistics (e.g., age distribution, gender breakdown, country distribution)
3. Any interesting patterns or insights you notice
4. Data quality observations (missing values, outliers, etc.)
5. Recommendations for further analysis

Keep your analysis clear and concise."""

# Send to LLM for analysis
print("Analyzing CSV data with LLM...")
print("-" * 80)

response = client.responses.create(
    model="gpt-4.1-mini",
    input=prompt
)

# Print the analysis
print(response.output_text)
print("-" * 80)
print(f"\nAnalysis completed for {row_count} records from {csv_file_path}")
```

After the API call the script prints the model’s analysis and a short completion message.  
It’s a simple orchestration for quick, high-level exploratory summaries rather than exhaustive  
statistical processing—intended to run locally with configured API credentials and best used as  
a starting point for deeper analysis.

## Analyze data with PandasAI
### LLM Integration for Data Analysis

PandasAI uses large language models to:  

1. **Understand Intent**: Parse your natural language question  
2. **Generate Code**: Create appropriate Pandas operations  
3. **Execute**: Run the generated code on your DataFrame  
4. **Format Results**: Present the answer in a readable format  

The LLM acts as a translator between human language and Pandas syntax. It  
considers the structure of your data, including column names and types, to  
generate accurate queries.  

### Key Classes and Functions

**Agent**: The main class for interacting with your data  

```python
from pandasai import Agent

agent = Agent(df, config={'llm': llm})
response = agent.chat("Your question here")
```

**LLM Configuration**: Specify which language model to use  

```python
# Configure PandasAI globally to use LiteLLM with OpenAI

llm = LiteLLM(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
pai.config.set({"llm": llm})
```

### Basic Usage

This example shows how to load a dataset and get a summary using natural  
language queries.  

```python
import pandas as pd
import pandasai as pai
from pandasai import Agent
from pandasai_litellm.litellm import LiteLLM
import os

# Configure PandasAI globally to use LiteLLM with OpenAI
llm = LiteLLM(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
pai.config.set({"llm": llm})

df = pd.DataFrame(
    {
        "employee": ["Alice", "Bob", "Charlie", "Diana"],
        "department": ["Sales", "IT", "Sales", "HR"],
        "salary": [75000, 85000, 70000, 65000],
    }
)


agent = Agent(df)
response = agent.chat("What is the average salary by department?")
print(response)
```

The agent analyzes your DataFrame, understands that revenue equals price times  
units_sold, generates the code `df['price'] * df['units_sold']`, and returns  
the calculated results.  

Expected output: A summary showing revenue per product calculated as price  
multiplied by units sold.  
