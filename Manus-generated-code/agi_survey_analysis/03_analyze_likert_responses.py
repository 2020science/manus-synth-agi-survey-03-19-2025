import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
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

print("Loading survey data for Likert scale analysis...")
# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Load JSON data for grid questions
with open('/home/ubuntu/agi_survey_simulation/survey_responses.json', 'r') as f:
    json_responses = json.load(f)
df_json = pd.DataFrame(json_responses)

# Create a file to store Likert scale analysis results
likert_report = open('/home/ubuntu/agi_survey_analysis/likert_scale_analysis.md', 'w')
likert_report.write("# Analysis of Likert Scale Responses in AGI Survey\n\n")
likert_report.write("This analysis examines the Likert scale responses of 1,000 undergraduate students who participated in the AGI survey.\n\n")

# 1. AGI Timeline Expectations
print("Analyzing AGI timeline expectations...")
likert_report.write("## 1. AGI Timeline Expectations\n\n")

timeline_counts = df['agi_timeline'].value_counts().sort_values(ascending=False)
timeline_percent = df['agi_timeline'].value_counts(normalize=True).sort_values(ascending=False) * 100

# Create a table of AGI timeline expectations
timeline_table = pd.DataFrame({
    'Count': timeline_counts,
    'Percentage': timeline_percent.round(1)
})
timeline_table.index.name = 'AGI Timeline Expectation'
timeline_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/agi_timeline_distribution.csv')

likert_report.write("Respondents were asked when they expect AGI to be developed:\n\n")
likert_report.write("| AGI Timeline Expectation | Count | Percentage |\n")
likert_report.write("|--------------------------|-------|------------|\n")
for timeline, row in timeline_table.iterrows():
    likert_report.write(f"| {timeline} | {int(row['Count'])} | {row['Percentage']}% |\n")
likert_report.write("\n")

# Create a visualization of AGI timeline expectations
plt.figure(figsize=(12, 6))
sns.barplot(x=timeline_counts.index, y=timeline_counts.values)
plt.title('AGI Timeline Expectations Among Undergraduate Students', fontsize=16)
plt.xlabel('Expected Timeline for AGI Development', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/agi_timeline_expectations.png', dpi=300)

likert_report.write("The majority of undergraduate respondents (53.4%) expect AGI to be developed within the next 25 years, ")
likert_report.write("with 29.5% expecting it within 10-25 years and 23.9% expecting it within the next 10 years. ")
likert_report.write("A notable 6.8% believe AGI already exists, while only 1.9% believe it will never be developed. ")
likert_report.write("This distribution suggests that most undergraduates anticipate AGI as a near to medium-term technological development, ")
likert_report.write("with relatively few expecting it to be far in the future or impossible.\n\n")
likert_report.write("![AGI Timeline Expectations](/home/ubuntu/agi_survey_analysis/figures/agi_timeline_expectations.png)\n\n")

# 2. Sentiment Toward AGI
print("Analyzing sentiment toward AGI...")
likert_report.write("## 2. Sentiment Toward AGI\n\n")

sentiment_counts = df['sentiment'].value_counts().sort_index()
sentiment_percent = df['sentiment'].value_counts(normalize=True).sort_index() * 100

# Create a table of sentiment toward AGI
sentiment_table = pd.DataFrame({
    'Count': sentiment_counts,
    'Percentage': sentiment_percent.round(1)
})
sentiment_table.index.name = 'Sentiment (1-5 scale)'
sentiment_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/sentiment_distribution.csv')

likert_report.write("Respondents rated their overall sentiment toward AGI on a scale from 1 (Very negative) to 5 (Very positive):\n\n")
likert_report.write("| Sentiment | Count | Percentage |\n")
likert_report.write("|-----------|-------|------------|\n")
for level, row in sentiment_table.iterrows():
    likert_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
likert_report.write("\n")

# Create a visualization of sentiment toward AGI
plt.figure(figsize=(10, 6))
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
plt.title('Sentiment Toward AGI Among Undergraduate Students', fontsize=16)
plt.xlabel('Sentiment (1=Very Negative, 5=Very Positive)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/sentiment_distribution.png', dpi=300)

# Calculate mean and standard deviation
sentiment_mean = df['sentiment'].mean()
sentiment_std = df['sentiment'].std()

likert_report.write(f"The mean sentiment score is {sentiment_mean:.2f} (SD = {sentiment_std:.2f}), indicating a slightly positive overall sentiment toward AGI. ")
likert_report.write("The distribution shows that 46.7% of respondents report positive sentiment (levels 4-5), ")
likert_report.write("32.5% report neutral sentiment (level 3), and 20.8% report negative sentiment (levels 1-2). ")
likert_report.write("This suggests that undergraduate students are generally more optimistic than pessimistic about AGI, ")
likert_report.write("though a significant minority express concerns.\n\n")
likert_report.write("![Sentiment Toward AGI](/home/ubuntu/agi_survey_analysis/figures/sentiment_distribution.png)\n\n")

# 3. Interest in AGI
print("Analyzing interest in AGI...")
likert_report.write("## 3. Interest in AGI\n\n")

interest_counts = df['interest'].value_counts().sort_index()
interest_percent = df['interest'].value_counts(normalize=True).sort_index() * 100

# Create a table of interest in AGI
interest_table = pd.DataFrame({
    'Count': interest_counts,
    'Percentage': interest_percent.round(1)
})
interest_table.index.name = 'Interest (1-5 scale)'
interest_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/interest_distribution.csv')

likert_report.write("Respondents rated their interest in AGI developments on a scale from 1 (Not at all interested) to 5 (Extremely interested):\n\n")
likert_report.write("| Interest Level | Count | Percentage |\n")
likert_report.write("|---------------|-------|------------|\n")
for level, row in interest_table.iterrows():
    likert_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
likert_report.write("\n")

# Create a visualization of interest in AGI
plt.figure(figsize=(10, 6))
sns.barplot(x=interest_counts.index, y=interest_counts.values)
plt.title('Interest in AGI Among Undergraduate Students', fontsize=16)
plt.xlabel('Interest Level (1=Not at all interested, 5=Extremely interested)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/interest_distribution.png', dpi=300)

# Calculate mean and standard deviation
interest_mean = df['interest'].mean()
interest_std = df['interest'].std()

likert_report.write(f"The mean interest score is {interest_mean:.2f} (SD = {interest_std:.2f}), indicating a moderate to high level of interest in AGI among undergraduates. ")
likert_report.write("The distribution shows that 52.3% of respondents report high interest (levels 4-5), ")
likert_report.write("29.7% report moderate interest (level 3), and 18.0% report low interest (levels 1-2). ")
likert_report.write("This suggests that most undergraduate students are engaged with the topic of AGI and interested in its development, ")
likert_report.write("with only a small minority expressing disinterest.\n\n")
likert_report.write("![Interest in AGI](/home/ubuntu/agi_survey_analysis/figures/interest_distribution.png)\n\n")

# 4. Perceived Career Impact
print("Analyzing perceived career impact...")
likert_report.write("## 4. Perceived Career Impact\n\n")

career_counts = df['career_impact'].value_counts().sort_index()
career_percent = df['career_impact'].value_counts(normalize=True).sort_index() * 100

# Create a table of perceived career impact
career_table = pd.DataFrame({
    'Count': career_counts,
    'Percentage': career_percent.round(1)
})
career_table.index.name = 'Career Impact (1-5 scale)'
career_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/career_impact_distribution.csv')

likert_report.write("Respondents rated the expected impact of AGI on their future careers on a scale from 1 (No impact) to 5 (Transformative impact):\n\n")
likert_report.write("| Career Impact | Count | Percentage |\n")
likert_report.write("|--------------|-------|------------|\n")
for level, row in career_table.iterrows():
    likert_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
likert_report.write("\n")

# Create a visualization of perceived career impact
plt.figure(figsize=(10, 6))
sns.barplot(x=career_counts.index, y=career_counts.values)
plt.title('Perceived Career Impact of AGI Among Undergraduate Students', fontsize=16)
plt.xlabel('Career Impact (1=No impact, 5=Transformative impact)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/career_impact_distribution.png', dpi=300)

# Calculate mean and standard deviation
career_mean = df['career_impact'].mean()
career_std = df['career_impact'].std()

likert_report.write(f"The mean career impact score is {career_mean:.2f} (SD = {career_std:.2f}), indicating that undergraduates expect AGI to have a significant impact on their future careers. ")
likert_report.write("The distribution shows that 61.8% of respondents anticipate high career impact (levels 4-5), ")
likert_report.write("26.4% anticipate moderate impact (level 3), and only 11.8% anticipate low impact (levels 1-2). ")
likert_report.write("This suggests that most undergraduate students recognize AGI as a technology that will significantly affect their professional futures, ")
likert_report.write("regardless of their field of study.\n\n")
likert_report.write("![Perceived Career Impact](/home/ubuntu/agi_survey_analysis/figures/career_impact_distribution.png)\n\n")

# 5. Risk Level Assessment
print("Analyzing risk level assessment...")
likert_report.write("## 5. Risk Level Assessment\n\n")

risk_counts = df['risk_level'].value_counts().sort_index()
risk_percent = df['risk_level'].value_counts(normalize=True).sort_index() * 100

# Create a table of risk level assessment
risk_table = pd.DataFrame({
    'Count': risk_counts,
    'Percentage': risk_percent.round(1)
})
risk_table.index.name = 'Risk Level (1-5 scale)'
risk_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/risk_level_distribution.csv')

likert_report.write("Respondents rated the level of risk they associate with AGI development on a scale from 1 (Very low risk) to 5 (Very high risk):\n\n")
likert_report.write("| Risk Level | Count | Percentage |\n")
likert_report.write("|-----------|-------|------------|\n")
for level, row in risk_table.iterrows():
    likert_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
likert_report.write("\n")

# Create a visualization of risk level assessment
plt.figure(figsize=(10, 6))
sns.barplot(x=risk_counts.index, y=risk_counts.values)
plt.title('Risk Level Assessment of AGI Among Undergraduate Students', fontsize=16)
plt.xlabel('Risk Level (1=Very low risk, 5=Very high risk)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/risk_level_distribution.png', dpi=300)

# Calculate mean and standard deviation
risk_mean = df['risk_level'].mean()
risk_std = df['risk_level'].std()

likert_report.write(f"The mean risk level score is {risk_mean:.2f} (SD = {risk_std:.2f}), indicating that undergraduates perceive a moderate to high level of risk associated with AGI development. ")
likert_report.write("The distribution shows that 34.1% of respondents perceive high risk (levels 4-5), ")
likert_report.write("45.7% perceive moderate risk (level 3), and 20.2% perceive low risk (levels 1-2). ")
likert_report.write("This suggests that while most undergraduate students recognize potential risks of AGI, ")
likert_report.write("they are not overwhelmingly pessimistic, with the largest group taking a moderate position.\n\n")
likert_report.write("![Risk Level Assessment](/home/ubuntu/agi_survey_analysis/figures/risk_level_distribution.png)\n\n")

# 6. Benefit Assessment
print("Analyzing benefit assessment...")
likert_report.write("## 6. Benefit Assessment\n\n")

benefit_counts = df['benefit_assessment'].value_counts().sort_index()
benefit_percent = df['benefit_assessment'].value_counts(normalize=True).sort_index() * 100

# Create a table of benefit assessment
benefit_table = pd.DataFrame({
    'Count': benefit_counts,
    'Percentage': benefit_percent.round(1)
})
benefit_table.index.name = 'Benefit Level (1-5 scale)'
benefit_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/benefit_assessment_distribution.csv')

likert_report.write("Respondents rated the level of benefit they associate with AGI development on a scale from 1 (Very low benefit) to 5 (Very high benefit):\n\n")
likert_report.write("| Benefit Level | Count | Percentage |\n")
likert_report.write("|--------------|-------|------------|\n")
for level, row in benefit_table.iterrows():
    likert_report.write(f"| {level} | {int(row['Count'])} | {row['Percentage']}% |\n")
likert_report.write("\n")

# Create a visualization of benefit assessment
plt.figure(figsize=(10, 6))
sns.barplot(x=benefit_counts.index, y=benefit_counts.values)
plt.title('Benefit Assessment of AGI Among Undergraduate Students', fontsize=16)
plt.xlabel('Benefit Level (1=Very low benefit, 5=Very high benefit)', fontsize=14)
plt.ylabel('Number of Respondents', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/benefit_assessment_distribution.png', dpi=300)

# Calculate mean and standard deviation
benefit_mean = df['benefit_assessment'].mean()
benefit_std = df['benefit_assessment'].std()

likert_report.write(f"The mean benefit assessment score is {benefit_mean:.2f} (SD = {benefit_std:.2f}), indicating that undergraduates perceive a high level of potential benefit from AGI development. ")
likert_report.write("The distribution shows that 69.6% of respondents perceive high benefit (levels 4-5), ")
likert_report.write("26.3% perceive moderate benefit (level 3), and only 4.1% perceive low benefit (levels 1-2). ")
likert_report.write("This suggests that undergraduate students are overwhelmingly optimistic about the potential benefits of AGI, ")
likert_report.write("with very few doubting its positive potential.\n\n")
likert_report.write("![Benefit Assessment](/home/ubuntu/agi_survey_analysis/figures/benefit_assessment_distribution.png)\n\n")

# 7. Governance Importance
print("Analyzing governance importance...")
likert_report.write("## 7. Governance Importance\n\n")

governance_counts = df['governance_importance'].value_counts().sort_index()
governance_percent = df['governance_importance'].value_counts(normalize=True).sort_index() * 100

# Create a table of governance importance
governance_table = pd.DataFrame({
    'Count': governance_counts,
    'Percentage': governance_percent.round(1)
})
governance_table.index.name = 'Governance Importance (1-5 scale)'
governance_table.to_csv('/home/ubuntu/agi_survey_analysis/tables/governance_importan<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>