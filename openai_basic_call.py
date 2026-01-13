from openai import OpenAI
import os

# Nahraď 'your-api-key-here' svojím skutočným OpenAI API kľúčom

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Konkrétny prompt
prompt = "Napíš krátky príbeh o programátorovi, ktorý objaví AI."

# Volanie API s system message pre kontext
response = client.chat.completions.create(
    model="mistralai/devstral-2512:free",
    messages=[
        {"role": "system", "content": "Si pomocný AI asistent, ktorý odpovedá v slovenčine."},
        {"role": "user", "content": prompt}
    ]
)

# Výpis výsledku
print(response.choices[0].message.content)