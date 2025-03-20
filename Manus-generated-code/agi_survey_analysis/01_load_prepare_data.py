import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re
import os

# Create directory for analysis outputs
os.makedirs('/home/ubuntu/agi_survey_analysis/figures', exist_ok=True)
os.makedirs('/home/ubuntu/agi_survey_analysis/tables', exist_ok=True)

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Load the data
print("Loading simulated survey data...")
df_responses = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')
with open('/home/ubuntu/agi_survey_simulation/survey_responses.json', 'r') as f:
    json_responses = json.load(f)

# Convert JSON data to DataFrame for easier analysis of nested structures
df_json = pd.DataFrame(json_responses)

# Print basic information about the dataset
print(f"Dataset contains {len(df_responses)} responses with {len(df_responses.columns)} variables")
print(f"Demographic variables: {[col for col in df_responses.columns if col.startswith(('age', 'gender', 'academic', 'field', 'ai_', 'technical', 'info_'))]}")
print(f"Opinion variables: {[col for col in df_responses.columns if not col.startswith(('age', 'gender', 'academic', 'field', 'ai_', 'technical', 'info_'))]}")

# Save the dataset information
with open('/home/ubuntu/agi_survey_analysis/dataset_info.txt', 'w') as f:
    f.write(f"Dataset contains {len(df_responses)} responses with {len(df_responses.columns)} variables\n\n")
    f.write("Demographic variables:\n")
    for col in [col for col in df_responses.columns if col.startswith(('age', 'gender', 'academic', 'field', 'ai_', 'technical', 'info_'))]:
        f.write(f"- {col}\n")
    f.write("\nOpinion variables:\n")
    for col in [col for col in df_responses.columns if not col.startswith(('age', 'gender', 'academic', 'field', 'ai_', 'technical', 'info_'))]:
        f.write(f"- {col}\n")

print("Data loaded and basic information extracted.")
print("Preparing data for analysis...")

# Prepare data for analysis
# Convert categorical variables to numeric for correlation analysis
categorical_vars = ['age', 'gender', 'academic_year', 'field_of_study', 'agi_timeline', 'responsibility', 'future_involvement', 'results_option']
for var in categorical_vars:
    if var in df_responses.columns:
        df_responses[f'{var}_code'] = df_responses[var].astype('category').cat.codes

# Create a clean numeric dataframe for statistical analysis
numeric_cols = ['ai_familiarity', 'technical_background', 'sentiment', 'interest', 
                'career_impact', 'risk_level', 'benefit_assessment', 'governance_importance', 
                'societal_preparation', 'education_need']
numeric_cols.extend([f'{var}_code' for var in categorical_vars if f'{var}_code' in df_responses.columns])

# Add information source columns
info_cols = [col for col in df_responses.columns if col.startswith('info_')]
numeric_cols.extend(info_cols)

# Create numeric dataframe
df_numeric = df_responses[numeric_cols].copy()

# Check for missing values
missing_values = df_numeric.isnull().sum()
print(f"Missing values in numeric data:\n{missing_values[missing_values > 0]}")

# Fill missing values if any
if missing_values.sum() > 0:
    df_numeric = df_numeric.fillna(df_numeric.mean())
    print("Missing values filled with column means")

print("Data preparation complete.")
print("Saving prepared data for further analysis...")

# Save prepared data
df_numeric.to_csv('/home/ubuntu/agi_survey_analysis/prepared_numeric_data.csv', index=False)
print("Prepared numeric data saved to /home/ubuntu/agi_survey_analysis/prepared_numeric_data.csv")

print("Data loading and preparation complete.")
