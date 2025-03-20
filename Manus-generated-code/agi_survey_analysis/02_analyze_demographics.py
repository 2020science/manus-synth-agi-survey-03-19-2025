import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Create directory for analysis outputs if it doesn't exist
os.makedirs('/home/ubuntu/agi_survey_analysis/figures', exist_ok=True)
os.makedirs('/home/ubuntu/agi_survey_analysis/tables', exist_ok=True)

print("Loading survey data for demographic analysis...")
# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Create a file to store demographic analysis results
demographic_report = open('/home/ubuntu/agi_survey_analysis/demographic_analysis.md', 'w')
demographic_report.write("# Demographic Analysis of AGI Survey Respondents\n\n")
demographic_report.write("This analysis examines the demographic characteristics of the 1,000 undergraduate students who participated in the AGI survey.\n\n")

# 1. Age Distribution
print("Analyzing age distribution...")
demographic_report.write("## 1. Age Distribution\n\n")

age_counts = df['age'].value_counts().sort_index()
age_percent = df['age'].value_counts(normalize=True).sort_index() * 100

# Create a table of age distribution
age_table = pd.DataFrame({
    'Count': age_counts,
    'Percentage': age_percent.round(1)
})
age_table.index.name = 'Age Group'
age_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/age_distribution.csv')

demographic_report.write("The age distribution of survey respondents reflects the typical undergraduate population at a public R1 university:\n\n")
demographic_report.write("| Age Group | Count | Percentage |\n")
demographic_report.write("|-----------|-------|------------|\n")
for age, row in age_table.iterrows():
    demographic_report.write(f"| {age} | {int(row['Count'])} | {row['Percentage']}% |\n")
demographic_report.write("\n")

# Create a visualization of age distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=age_counts.index, y=age_counts.values)
plt.title('Age Distribution of Survey Respondents', fontsize=16)
plt.xlabel('Age Group', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/age_distribution.png', dpi=300)

demographic_report.write("The majority of respondents (90.0%) are between 18-23 years old, which is consistent with the traditional undergraduate age range. ")
demographic_report.write("The largest age groups are 20-21 years (35.2%) and 18-19 years (31.9%), representing freshmen and sophomores. ")
demographic_report.write("Only a small percentage (10.0%) of respondents are 24 years or older, representing non-traditional students.\n\n")
demographic_report.write("![Age Distribution](/home/ubuntu/agi_survey_analysis/figures/age_distribution.png)\n\n")

# 2. Gender Distribution
print("Analyzing gender distribution...")
demographic_report.write("## 2. Gender Distribution\n\n")

gender_counts = df['gender'].value_counts()
gender_percent = df['gender'].value_counts(normalize=True) * 100

# Create a table of gender distribution
gender_table = pd.DataFrame({
    'Count': gender_counts,
    'Percentage': gender_percent.round(1)
})
gender_table.index.name = 'Gender'
gender_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/gender_distribution.csv')

demographic_report.write("The gender distribution of survey respondents shows:\n\n")
demographic_report.write("| Gender | Count | Percentage |\n")
demographic_report.write("|--------|-------|------------|\n")
for gender, row in gender_table.iterrows():
    demographic_report.write(f"| {gender} | {int(row['Count'])} | {row['Percentage']}% |\n")
demographic_report.write("\n")

# Create a visualization of gender distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=gender_counts.index, y=gender_counts.values)
plt.title('Gender Distribution of Survey Respondents', fontsize=16)
plt.xlabel('Gender', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/gender_distribution.png', dpi=300)

demographic_report.write("The gender distribution is relatively balanced, with a slightly higher percentage of female respondents (49.4%) compared to male respondents (45.8%). ")
demographic_report.write("This is consistent with recent trends in undergraduate enrollment at U.S. public universities, where women often slightly outnumber men. ")
demographic_report.write("A small percentage of respondents (3.3%) identified as non-binary/third gender, with even smaller percentages preferring to self-describe or not disclose their gender.\n\n")
demographic_report.write("![Gender Distribution](/home/ubuntu/agi_survey_analysis/figures/gender_distribution.png)\n\n")

# 3. Academic Year Distribution
print("Analyzing academic year distribution...")
demographic_report.write("## 3. Academic Year Distribution\n\n")

year_counts = df['academic_year'].value_counts().sort_values(ascending=False)
year_percent = df['academic_year'].value_counts(normalize=True).sort_values(ascending=False) * 100

# Create a table of academic year distribution
year_table = pd.DataFrame({
    'Count': year_counts,
    'Percentage': year_percent.round(1)
})
year_table.index.name = 'Academic Year'
year_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/academic_year_distribution.csv')

demographic_report.write("The distribution of respondents across academic years shows:\n\n")
demographic_report.write("| Academic Year | Count | Percentage |\n")
demographic_report.write("|--------------|-------|------------|\n")
for year, row in year_table.iterrows():
    demographic_report.write(f"| {year} | {int(row['Count'])} | {row['Percentage']}% |\n")
demographic_report.write("\n")

# Create a visualization of academic year distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title('Academic Year Distribution of Survey Respondents', fontsize=16)
plt.xlabel('Academic Year', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/academic_year_distribution.png', dpi=300)

demographic_report.write("The survey captured responses from students across all academic years, with the highest representation from freshmen (32.0%). ")
demographic_report.write("Sophomores, juniors, and seniors each represent approximately 20-23% of respondents, providing a good cross-section of undergraduate perspectives at different stages of their academic careers. ")
demographic_report.write("The higher percentage of freshmen may reflect their greater availability or willingness to participate in surveys.\n\n")
demographic_report.write("![Academic Year Distribution](/home/ubuntu/agi_survey_analysis/figures/academic_year_distribution.png)\n\n")

# 4. Field of Study Distribution
print("Analyzing field of study distribution...")
demographic_report.write("## 4. Field of Study Distribution\n\n")

field_counts = df['field_of_study'].value_counts()
field_percent = df['field_of_study'].value_counts(normalize=True) * 100

# Create a table of field of study distribution
field_table = pd.DataFrame({
    'Count': field_counts,
    'Percentage': field_percent.round(1)
})
field_table.index.name = 'Field of Study'
field_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/field_of_study_distribution.csv')

demographic_report.write("The distribution of respondents across fields of study shows:\n\n")
demographic_report.write("| Field of Study | Count | Percentage |\n")
demographic_report.write("|---------------|-------|------------|\n")
for field, row in field_table.iterrows():
    demographic_report.write(f"| {field} | {int(row['Count'])} | {row['Percentage']}% |\n")
demographic_report.write("\n")

# Create a visualization of field of study distribution
plt.figure(figsize=(12, 6))
sns.barplot(x=field_counts.index, y=field_counts.values)
plt.title('Field of Study Distribution of Survey Respondents', fontsize=16)
plt.xlabel('Field of Study', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/field_of_study_distribution.png', dpi=300)

demographic_report.write("The survey captured a diverse range of academic disciplines, with Social Sciences having the highest representation (21.8%), ")
demographic_report.write("followed by Business/Economics (15.1%), Natural Sciences (14.5%), and Arts and Humanities (14.3%). ")
demographic_report.write("Technical fields like Engineering (12.0%) and Computer Science/IT (10.5%) are also well-represented, ")
demographic_report.write("while Health Sciences (7.6%) and Education (3.2%) have smaller but still significant representation. ")
demographic_report.write("This distribution broadly reflects the typical enrollment patterns at public R1 universities, ")
demographic_report.write("though the exact proportions may vary by institution.\n\n")
demographic_report.write("![Field of Study Distribution](/home/ubuntu/agi_survey_analysis/figures/field_of_study_distribution.png)\n\n")

# 5. AI Familiarity Distribution
print("Analyzing AI familiarity distribution...")
demographic_report.write("## 5. AI Familiarity Distribution\n\n")

familiarity_counts = df['ai_familiarity'].value_counts().sort_index()
familiarity_percent = df['ai_familiarity'].value_counts(normalize=True).sort_index() * 100

# Create a table of AI familiarity distribution
familiarity_table = pd.DataFrame({
    'Count': familiarity_counts,
    'Percentage': familiarity_percent.round(1)
})
familiarity_table.index.name = 'AI Familiarity (1-5 scale)'
familiarity_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/ai_familiarity_distribution.csv')

demographic_report.write("Respondents rated their familiarity with AI on a scale from 1 (Not at all familiar) to 5 (Extremely familiar):\n\n")
demographic_report.write("| AI Familiarity | Count | Percentage |\n")
demographic_report.write("|---------------|-------|------------|\n")
for level, row in familiarity_table.iterrows():
    demographic_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
demographic_report.write("\n")

# Create a visualization of AI familiarity distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=familiarity_counts.index, y=familiarity_counts.values)
plt.title('AI Familiarity Distribution of Survey Respondents', fontsize=16)
plt.xlabel('AI Familiarity (1-5 scale)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/ai_familiarity_distribution.png', dpi=300)

# Calculate mean and standard deviation
ai_familiarity_mean = df['ai_familiarity'].mean()
ai_familiarity_std = df['ai_familiarity'].std()

demographic_report.write(f"The mean AI familiarity score is {ai_familiarity_mean:.2f} (SD = {ai_familiarity_std:.2f}), indicating a moderate level of familiarity overall. ")
demographic_report.write("The distribution shows that 48.2% of respondents report low familiarity (levels 1-2), ")
demographic_report.write("21.5% report moderate familiarity (level 3), and 30.3% report high familiarity (levels 4-5). ")
demographic_report.write("This distribution suggests that while most undergraduates have some awareness of AI, ")
demographic_report.write("fewer have in-depth knowledge or experience with the technology.\n\n")
demographic_report.write("![AI Familiarity Distribution](/home/ubuntu/agi_survey_analysis/figures/ai_familiarity_distribution.png)\n\n")

# 6. Technical Background Distribution
print("Analyzing technical background distribution...")
demographic_report.write("## 6. Technical Background Distribution\n\n")

technical_counts = df['technical_background'].value_counts().sort_index()
technical_percent = df['technical_background'].value_counts(normalize=True).sort_index() * 100

# Create a table of technical background distribution
technical_table = pd.DataFrame({
    'Count': technical_counts,
    'Percentage': technical_percent.round(1)
})
technical_table.index.name = 'Technical Background (1-5 scale)'
technical_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/technical_background_distribution.csv')

demographic_report.write("Respondents rated their technical background on a scale from 1 (Non-technical) to 5 (Highly technical):\n\n")
demographic_report.write("| Technical Background | Count | Percentage |\n")
demographic_report.write("|--------------------|-------|------------|\n")
for level, row in technical_table.iterrows():
    demographic_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
demographic_report.write("\n")

# Create a visualization of technical background distribution
plt.figure(figsize=(10, 6))
sns.barplot(x=technical_counts.index, y=technical_counts.values)
plt.title('Technical Background Distribution of Survey Respondents', fontsize=16)
plt.xlabel('Technical Background (1-5 scale)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/technical_background_distribution.png', dpi=300)

# Calculate mean and standard deviation
technical_mean = df['technical_background'].mean()
technical_std = df['technical_background'].std()

demographic_report.write(f"The mean technical background score is {technical_mean:.2f} (SD = {technical_std:.2f}), indicating a slightly below-moderate level of technical expertise. ")
demographic_report.write("The distribution shows that 42.8% of respondents report low technical background (levels 1-2), ")
demographic_report.write("29.2% report moderate technical background (level 3), and 28.0% report high technical background (levels 4-5). ")
demographic_report.write("This distribution is consistent with the mix of technical and non-technical majors represented in the sample.\n\n")
demographic_report.write("![Technical Background Distribution](/home/ubuntu/agi_survey_analysis/figures/technical_background_distribution.png)\n\n")

# 7. Information Sources Distribution
print("Analyzing information sources distribution...")
demographic_report.write("## 7. Information Sources Distribution\n\n")

# Extract information source columns
info_cols = [col for col in df.columns if col.startswith('info_')]
info_sources = {}

for col in info_cols:
    # Clean up the column name for display
    source_name = col.replace('info_', '').replace('_', ' ')
    info_sources[source_name] = df[col].sum()

# Sort by frequency
info_sources = {k: v for k, v in sorted(info_sources.items(), key=lambda item: item[1], reverse=True)}

# Calculate percentages
total_respondents = len(df)
info_percentages = {k: (v / total_respondents) * 100 for k, v in info_sources.items()}

# Create a table of information sources
info_table = pd.DataFrame({
    'Count': info_sources.values(),
    'Percentage': [round(p, 1) for p in info_percentages.values()]
}, index=info_sources.keys())
info_table.index.name = 'Information Source'
info_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/information_sources_distribution.csv')

demographic_report.write("Respondents indicated their sources of information about AI (multiple selections allowed):\n\n")
demographic_report.write("| Information Source | Count | Percentage |\n")
demographic_report.write("|-------------------|-------|------------|\n")
for source, count in info_sources.items():
    percentage = info_percentages[source]
    demographic_report.write(f"| {source} | {count} | {percentage:.1f}% |\n")
demographic_report.write("\n")

# Create a visualization of inform<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>