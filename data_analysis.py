import pandas as pd
import os

def load_data(file_path):
    """
    Load CSV data and handle missing values.
    For numerical columns, fill missing values with median.
    For categorical columns, drop rows with missing values.
    """
    try:
        df = pd.read_csv(file_path)
        # Handle missing values
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df.dropna(subset=[col], inplace=True)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def numerical_analysis(df, col):
    """
    Perform statistical analysis on a numerical column.
    Returns a dictionary with various statistics.
    """
    data = df[col].dropna()
    if data.empty:
        return {}
    
    mean = data.mean()
    median = data.median()
    mode = data.mode().iloc[0] if not data.mode().empty else 'N/A'
    std = data.std()
    var = data.var()
    min_val = data.min()
    max_val = data.max()
    range_val = max_val - min_val
    p25 = data.quantile(0.25)
    p50 = data.quantile(0.5)
    p75 = data.quantile(0.75)
    
    return {
        'Mean': mean,
        'Median': median,
        'Mode': mode,
        'Standard Deviation': std,
        'Variance': var,
        'Min': min_val,
        'Max': max_val,
        'Range': range_val,
        '25th Percentile': p25,
        '50th Percentile': p50,
        '75th Percentile': p75
    }

def categorical_analysis(df, col):
    """
    Perform frequency analysis on a categorical column.
    Returns a DataFrame with top 5 values, counts, and percentages.
    """
    counts = df[col].value_counts()
    top5 = counts.head(5)
    total = len(df)
    percentages = (top5 / total * 100).round(2)
    return pd.DataFrame({'Count': top5, 'Percentage': percentages})

def generate_markdown_report(df, num_stats, cat_stats, output_file):
    """
    Generate the Markdown report with analysis findings.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# User Data Analysis Report\n\n")
        
        # Data Overview
        f.write("## Data Overview\n\n")
        f.write(f"- **Total Records:** {len(df)}\n")
        f.write(f"- **Total Columns:** {len(df.columns)}\n\n")
        
        # Numerical Columns Statistics
        f.write("## Numerical Columns Statistics\n\n")
        for col, stats in num_stats.items():
            f.write(f"### {col}\n\n")
            table = "| Statistic | Value |\n|-----------|-------|\n"
            for stat, val in stats.items():
                if isinstance(val, (int, float)) and not pd.isna(val):
                    table += f"| {stat} | {val:.2f} |\n"
                else:
                    table += f"| {stat} | {val} |\n"
            f.write(table + "\n")
        
        # Categorical Columns Analysis
        f.write("## Categorical Columns Analysis\n\n")
        for col, df_stats in cat_stats.items():
            f.write(f"### {col}\n\n")
            table = "| Value | Count | Percentage |\n|-------|-------|------------|\n"
            for idx, row in df_stats.iterrows():
                table += f"| {idx} | {row['Count']} | {row['Percentage']:.2f}% |\n"
            f.write(table + "\n")

def main():
    """
    Main function to orchestrate the data analysis.
    """
    file_path = 'users_data4.csv'
    output_file = 'users_analysis.md'
    
    # Load data
    df = load_data(file_path)
    if df is None:
        return
    
    # Identify column types
    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(exclude=['number']).columns
    
    # Perform numerical analysis
    num_stats = {}
    for col in num_cols:
        num_stats[col] = numerical_analysis(df, col)
    
    # Perform categorical analysis
    cat_stats = {}
    for col in cat_cols:
        cat_stats[col] = categorical_analysis(df, col)
    
    # Generate report
    generate_markdown_report(df, num_stats, cat_stats, output_file)
    print(f"Analysis report generated: {output_file}")

if __name__ == "__main__":
    main()