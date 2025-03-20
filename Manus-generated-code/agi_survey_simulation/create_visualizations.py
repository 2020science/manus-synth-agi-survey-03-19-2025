import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# Create directory for visualizations
os.makedirs('/home/ubuntu/agi_survey_simulation/visualizations', exist_ok=True)

# Load the simulated responses
with open('/home/ubuntu/agi_survey_simulation/survey_responses.json', 'r') as f:
    responses = json.load(f)

df = pd.DataFrame(responses)

# Create demographic visualizations
plt.figure(figsize=(12, 8))

# Age distribution
plt.subplot(2, 2, 1)
age_counts = df['age'].value_counts().sort_index()
sns.barplot(x=age_counts.index, y=age_counts.values)
plt.title('Age Distribution')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Gender distribution
plt.subplot(2, 2, 2)
gender_counts = df['gender'].value_counts()
sns.barplot(x=gender_counts.index, y=gender_counts.values)
plt.title('Gender Distribution')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Academic year distribution
plt.subplot(2, 2, 3)
year_counts = df['academic_year'].value_counts().sort_index()
sns.barplot(x=year_counts.index, y=year_counts.values)
plt.title('Academic Year Distribution')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Field of study distribution
plt.subplot(2, 2, 4)
field_counts = df['field_of_study'].value_counts()
sns.barplot(x=field_counts.index, y=field_counts.values)
plt.title('Field of Study Distribution')
plt.ylabel('Count')
plt.xticks(rotation=90)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_simulation/visualizations/demographic_distribution.png')

# Create opinion visualizations
plt.figure(figsize=(14, 10))

# AGI Timeline
plt.subplot(2, 2, 1)
timeline_counts = df['agi_timeline'].value_counts().sort_values(ascending=False)
sns.barplot(x=timeline_counts.index, y=timeline_counts.values)
plt.title('AGI Timeline Expectations')
plt.ylabel('Count')
plt.xticks(rotation=90)

# Sentiment toward AGI
plt.subplot(2, 2, 2)
sentiment_counts = df['sentiment'].value_counts().sort_index()
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
plt.title('Sentiment Toward AGI (1-5 Scale)')
plt.ylabel('Count')
plt.xlabel('Sentiment (1=Very Negative, 5=Very Positive)')

# Risk Level Assessment
plt.subplot(2, 2, 3)
risk_counts = df['risk_level'].value_counts().sort_index()
sns.barplot(x=risk_counts.index, y=risk_counts.values)
plt.title('Risk Level Assessment (1-5 Scale)')
plt.ylabel('Count')
plt.xlabel('Risk Level (1=Very Low, 5=Very High)')

# Benefit Assessment
plt.subplot(2, 2, 4)
benefit_counts = df['benefit_assessment'].value_counts().sort_index()
sns.barplot(x=benefit_counts.index, y=benefit_counts.values)
plt.title('Benefit Assessment (1-5 Scale)')
plt.ylabel('Count')
plt.xlabel('Benefit Level (1=Very Low, 5=Very High)')

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_simulation/visualizations/opinion_distribution.png')

# Create correlation heatmap
plt.figure(figsize=(12, 10))
numeric_cols = ['ai_familiarity', 'technical_background', 'sentiment', 
                'interest', 'career_impact', 'risk_level', 
                'benefit_assessment', 'governance_importance', 
                'societal_preparation', 'education_need']
corr = df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
plt.title('Correlation Between Key Opinion Variables')
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_simulation/visualizations/correlation_heatmap.png')

# Create field of study vs. opinion variables
plt.figure(figsize=(14, 10))

# Field vs. AGI Timeline
plt.subplot(2, 2, 1)
field_timeline = pd.crosstab(df['field_of_study'], df['agi_timeline'], normalize='index')
field_timeline.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('AGI Timeline Expectations by Field of Study')
plt.ylabel('Proportion')
plt.xticks(rotation=90)
plt.legend(title='Timeline', bbox_to_anchor=(1.05, 1), loc='upper left')

# Field vs. Sentiment
plt.subplot(2, 2, 2)
field_sentiment = df.groupby('field_of_study')['sentiment'].mean().sort_values(ascending=False)
sns.barplot(x=field_sentiment.index, y=field_sentiment.values)
plt.title('Average Sentiment Toward AGI by Field of Study')
plt.ylabel('Average Sentiment (1-5)')
plt.xticks(rotation=90)

# Field vs. Risk Level
plt.subplot(2, 2, 3)
field_risk = df.groupby('field_of_study')['risk_level'].mean().sort_values(ascending=False)
sns.barplot(x=field_risk.index, y=field_risk.values)
plt.title('Average Risk Assessment by Field of Study')
plt.ylabel('Average Risk Level (1-5)')
plt.xticks(rotation=90)

# Field vs. Benefit Assessment
plt.subplot(2, 2, 4)
field_benefit = df.groupby('field_of_study')['benefit_assessment'].mean().sort_values(ascending=False)
sns.barplot(x=field_benefit.index, y=field_benefit.values)
plt.title('Average Benefit Assessment by Field of Study')
plt.ylabel('Average Benefit Level (1-5)')
plt.xticks(rotation=90)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_simulation/visualizations/field_vs_opinions.png')

# Create AI familiarity vs. opinion variables
plt.figure(figsize=(14, 10))

# Familiarity vs. AGI Timeline
plt.subplot(2, 2, 1)
familiarity_timeline = pd.crosstab(df['ai_familiarity'], df['agi_timeline'], normalize='index')
familiarity_timeline.plot(kind='bar', stacked=True, ax=plt.gca())
plt.title('AGI Timeline Expectations by AI Familiarity')
plt.ylabel('Proportion')
plt.xlabel('AI Familiarity (1-5)')
plt.legend(title='Timeline', bbox_to_anchor=(1.05, 1), loc='upper left')

# Familiarity vs. Sentiment
plt.subplot(2, 2, 2)
familiarity_sentiment = df.groupby('ai_familiarity')['sentiment'].mean()
sns.barplot(x=familiarity_sentiment.index, y=familiarity_sentiment.values)
plt.title('Average Sentiment Toward AGI by AI Familiarity')
plt.ylabel('Average Sentiment (1-5)')
plt.xlabel('AI Familiarity (1-5)')

# Familiarity vs. Risk Level
plt.subplot(2, 2, 3)
familiarity_risk = df.groupby('ai_familiarity')['risk_level'].mean()
sns.barplot(x=familiarity_risk.index, y=familiarity_risk.values)
plt.title('Average Risk Assessment by AI Familiarity')
plt.ylabel('Average Risk Level (1-5)')
plt.xlabel('AI Familiarity (1-5)')

# Familiarity vs. Benefit Assessment
plt.subplot(2, 2, 4)
familiarity_benefit = df.groupby('ai_familiarity')['benefit_assessment'].mean()
sns.barplot(x=familiarity_benefit.index, y=familiarity_benefit.values)
plt.title('Average Benefit Assessment by AI Familiarity')
plt.ylabel('Average Benefit Level (1-5)')
plt.xlabel('AI Familiarity (1-5)')

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_simulation/visualizations/familiarity_vs_opinions.png')

# Create responsibility and future involvement visualizations
plt.figure(figsize=(14, 6))

# Responsibility for AGI governance
plt.subplot(1, 2, 1)
responsibility_counts = df['responsibility'].value_counts()
sns.barplot(x=responsibility_counts.index, y=responsibility_counts.values)
plt.title('Who Should Be Primarily Responsible for AGI Governance')
plt.ylabel('Count')
plt.xticks(rotation=90)

# Future involvement
plt.subplot(1, 2, 2)
involvement_counts = df['future_involvement'].value_counts().sort_values()
sns.barplot(x=involvement_counts.index, y=involvement_counts.values)
plt.title('Likelihood of Future Involvement with AGI')
plt.ylabel('Count')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_simulation/visualizations/responsibility_and_involvement.png')

print("Created visualizations of simulated survey data in /home/ubuntu/agi_survey_simulation/visualizations/")
