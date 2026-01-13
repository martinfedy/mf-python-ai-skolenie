from pandasai import SmartDataframe
from pandasai_litellm.litellm import LiteLLM
from pandasai import Agent
import pandasai as pai
import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Initialize PandasAI with OpenAI (using OpenRouter)
llm = LiteLLM(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="openrouter/mistralai/mistral-7b-instruct:free"
    #,base_url="https://openrouter.ai/api/v1"
)

pai.config.set({"llm": llm})

# Load the CSV file
df = pd.read_csv('users_data4.csv')

# Basic data overview
total_records = len(df)
total_columns = len(df.columns)
columns = list(df.columns)

# Numerical columns statistics
numerical_stats = {}
for col in ['id', 'salary']:
    if col in df.columns:
        data = df[col].dropna()
        if len(data) > 0:
            stats = {
                'Priemer': round(data.mean(), 2),
                'Medián': round(data.median(), 2),
                'Modus': data.mode().iloc[0] if not data.mode().empty else 'N/A',
                'Štandardná odchýlka': round(data.std(), 2),
                'Minimálna hodnota': data.min(),
                'Maximálna hodnota': data.max(),
                'Rozsah': data.max() - data.min(),
                '25. percentil': round(data.quantile(0.25), 2),
                '75. percentil': round(data.quantile(0.75), 2)
            }
            numerical_stats[col] = stats

# Categorical columns analysis (top 5 for each)
categorical_analysis = {}
for col in ['first_name', 'last_name', 'email', 'occupation', 'created_at']:
    if col in df.columns:
        value_counts = df[col].value_counts().head(5)
        analysis = []
        for value, count in value_counts.items():
            percentage = round((count / total_records) * 100, 2)
            analysis.append({'Value': value, 'Count': count, 'Percentage': f'{percentage}%'})
        categorical_analysis[col] = analysis

# Generate plots
plt.figure(figsize=(10, 6))
df['salary'].hist(bins=10)
plt.title('Distribúcia platov')
plt.xlabel('Plat')
plt.ylabel('Počet')
plt.savefig('grafy/histogram_platov_pandasai.png')
plt.close()

# Top occupations
occupation_counts = df['occupation'].value_counts().head(5)
plt.figure(figsize=(10, 6))
occupation_counts.plot(kind='bar')
plt.title('Top 5 povolaní')
plt.xlabel('Povolanie')
plt.ylabel('Počet')
plt.xticks(rotation=45)
plt.savefig('grafy/top_povolania_pandasai.png')
plt.close()

# Salaries by date
df['created_at'] = pd.to_datetime(df['created_at'])
plt.figure(figsize=(10, 6))
plt.scatter(df['created_at'], df['salary'])
plt.title('Platy podľa dátumu vytvorenia')
plt.xlabel('Dátum')
plt.ylabel('Plat')
plt.xticks(rotation=45)
plt.savefig('grafy/platy_podla_datumu_pandasai.png')
plt.close()

# PandasAI Analysis
#df_ai = SmartDataframe(df, config={"llm": llm})
agent = Agent(df)

data_summary = f"""
Celkový počet záznamov: {total_records}
Počet stĺpcov: {total_columns}
Stĺpce: {', '.join(columns)}

Štatistiky pre salary:
Priemer: {numerical_stats.get('salary', {}).get('Priemer', 'N/A')}
Medián: {numerical_stats.get('salary', {}).get('Medián', 'N/A')}
Rozsah: {numerical_stats.get('salary', {}).get('Rozsah', 'N/A')}

Top povolania: {', '.join(occupation_counts.index.tolist())}
"""

prompt = f"""
Analyzujte nasledujúce dáta o používateľoch a poskytnite prehľadnú analýzu v slovenčine. Zahŕňajte trendy, zaujímavé poznatky a odporúčania.

{data_summary}

Poskytnite analýzu v niekoľkých odsekoch.
"""



try:
    ai_analysis = agent.chat(prompt)
except Exception as e:
    ai_analysis = f"Nebolo možné získať analýzu od PandasAI. Chyba: {str(e)}"

# Generate Markdown report
markdown_content = f"""# Analýza údajov používateľov pomocou PandasAI

*Vygenerované dňa: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Prehľad dát

- **Celkový počet záznamov:** {total_records}
- **Počet stĺpcov:** {total_columns}
- **Stĺpce:** {', '.join(columns)}

## Štatistiky numerických stĺpcov

"""

for col, stats in numerical_stats.items():
    markdown_content += f"### {col}\n\n| Štatistika | Hodnota |\n|------------|--------|\n"
    for stat, value in stats.items():
        markdown_content += f"| {stat} | {value} |\n"
    markdown_content += "\n"

markdown_content += "## Kategorické analýzy stĺpcov\n\n"

for col, analysis in categorical_analysis.items():
    markdown_content += f"### {col}\n\n| Hodnota | Počet | Percento |\n|---------|-------|----------|\n"
    for item in analysis:
        markdown_content += f"| {item['Value']} | {item['Count']} | {item['Percentage']} |\n"
    markdown_content += "\n"

markdown_content += """## Grafy

### Distribúcia platov

![Distribúcia platov](grafy/histogram_platov_pandasai.png)

### Top 5 povolaní

![Top 5 povolaní](grafy/top_povolania_pandasai.png)

### Platy podľa dátumu vytvorenia

![Platy podľa dátumu vytvorenia](grafy/platy_podla_datumu_pandasai.png)

## PandasAI Analýza

""" + str(ai_analysis)

# Write to file
with open('pandasai_user_analysis.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print("Analýza dokončená. Výstup uložený v pandasai_user_analysis.md")