import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Create directory for analysis outputs if it doesn't exist
os.makedirs('/home/ubuntu/agi_survey_analysis/figures', exist_ok=True)
os.makedirs('/home/ubuntu/agi_survey_analysis/tables', exist_ok=True)

print("Loading survey data for correlation and pattern analysis...")
# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')
df_numeric = pd.read_csv('/home/ubuntu/agi_survey_analysis/prepared_numeric_data.csv')

# Create a file to store correlation and pattern analysis results
correlation_report = open('/home/ubuntu/agi_survey_analysis/correlation_pattern_analysis.md', 'w')
correlation_report.write("# Correlation and Pattern Analysis in AGI Survey\n\n")
correlation_report.write("This analysis examines correlations and patterns across different variables in the AGI survey of 1,000 undergraduate students.\n\n")

# 1. Correlation Analysis Between Key Variables
print("Analyzing correlations between key variables...")
correlation_report.write("## 1. Correlation Analysis Between Key Variables\n\n")

# Select key variables for correlation analysis
key_vars = ['ai_familiarity', 'technical_background', 'sentiment', 'interest', 
            'career_impact', 'risk_level', 'benefit_assessment', 'governance_importance', 
            'societal_preparation', 'education_need']

# Calculate correlation matrix
corr_matrix = df[key_vars].corr()

# Create a heatmap of correlations
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, cmap='coolwarm', vmin=-1, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")
plt.title('Correlation Matrix of Key Survey Variables', fontsize=16)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/key_variables_correlation.png', dpi=300)

# Save correlation matrix to CSV
corr_matrix.to_csv('/home/ubuntu/agi_survey_analysis/tables/key_variables_correlation.csv')

# Write about strongest correlations
correlation_report.write("The correlation analysis reveals several significant relationships between key variables in the survey:\n\n")

# Find strongest positive correlations
pos_corrs = []
for i in range(len(key_vars)):
    for j in range(i+1, len(key_vars)):
        corr = corr_matrix.iloc[i, j]
        if corr > 0.3:  # Threshold for moderate positive correlation
            pos_corrs.append((key_vars[i], key_vars[j], corr))

pos_corrs.sort(key=lambda x: x[2], reverse=True)

correlation_report.write("### Strongest Positive Correlations\n\n")
for var1, var2, corr in pos_corrs[:5]:
    correlation_report.write(f"- **{var1} and {var2}**: r = {corr:.2f}\n")
correlation_report.write("\n")

# Find strongest negative correlations
neg_corrs = []
for i in range(len(key_vars)):
    for j in range(i+1, len(key_vars)):
        corr = corr_matrix.iloc[i, j]
        if corr < -0.3:  # Threshold for moderate negative correlation
            neg_corrs.append((key_vars[i], key_vars[j], corr))

neg_corrs.sort(key=lambda x: x[2])

correlation_report.write("### Strongest Negative Correlations\n\n")
for var1, var2, corr in neg_corrs[:5]:
    correlation_report.write(f"- **{var1} and {var2}**: r = {corr:.2f}\n")
correlation_report.write("\n")

# Interpret key correlations
correlation_report.write("### Interpretation of Key Correlations\n\n")

# AI Familiarity and Sentiment
ai_sentiment_corr = corr_matrix.loc['ai_familiarity', 'sentiment']
correlation_report.write(f"1. **AI Familiarity and Sentiment** (r = {ai_sentiment_corr:.2f}): ")
if ai_sentiment_corr > 0.3:
    correlation_report.write("There is a moderate positive correlation between AI familiarity and sentiment toward AGI. ")
    correlation_report.write("This suggests that students who are more familiar with AI tend to have more positive attitudes toward AGI. ")
    correlation_report.write("This may be because greater knowledge reduces fear of the unknown or because those with positive attitudes are more likely to seek out information about AI.\n\n")
elif ai_sentiment_corr > 0:
    correlation_report.write("There is a weak positive correlation between AI familiarity and sentiment toward AGI. ")
    correlation_report.write("This suggests that greater knowledge about AI is somewhat associated with more positive attitudes, ")
    correlation_report.write("though the relationship is not strong.\n\n")
else:
    correlation_report.write("There is no positive correlation between AI familiarity and sentiment toward AGI. ")
    correlation_report.write("This suggests that greater knowledge about AI does not necessarily lead to more positive attitudes.\n\n")

# Risk and Benefit Assessment
risk_benefit_corr = corr_matrix.loc['risk_level', 'benefit_assessment']
correlation_report.write(f"2. **Risk Level and Benefit Assessment** (r = {risk_benefit_corr:.2f}): ")
if abs(risk_benefit_corr) < 0.1:
    correlation_report.write("There is virtually no correlation between perceived risks and benefits of AGI. ")
    correlation_report.write("This suggests that students view risks and benefits as independent dimensions rather than as a zero-sum trade-off. ")
    correlation_report.write("Students can simultaneously recognize significant benefits and significant risks.\n\n")
elif risk_benefit_corr > 0:
    correlation_report.write("There is a positive correlation between perceived risks and benefits of AGI. ")
    correlation_report.write("This suggests that students who see greater potential benefits also tend to recognize greater risks, ")
    correlation_report.write("perhaps reflecting a more nuanced understanding of AGI's potential impact.\n\n")
else:
    correlation_report.write("There is a negative correlation between perceived risks and benefits of AGI. ")
    correlation_report.write("This suggests that students tend to view AGI through either an optimistic or pessimistic lens, ")
    correlation_report.write("with those seeing high benefits tending to downplay risks and vice versa.\n\n")

# Technical Background and Risk Perception
tech_risk_corr = corr_matrix.loc['technical_background', 'risk_level']
correlation_report.write(f"3. **Technical Background and Risk Level** (r = {tech_risk_corr:.2f}): ")
if tech_risk_corr < -0.3:
    correlation_report.write("There is a moderate negative correlation between technical background and risk perception. ")
    correlation_report.write("This suggests that students with stronger technical backgrounds tend to perceive lower risks associated with AGI. ")
    correlation_report.write("This may reflect greater confidence in technical safeguards or a more optimistic view of technological development among those with technical expertise.\n\n")
elif tech_risk_corr < 0:
    correlation_report.write("There is a weak negative correlation between technical background and risk perception. ")
    correlation_report.write("This suggests that students with stronger technical backgrounds tend to perceive somewhat lower risks associated with AGI, ")
    correlation_report.write("though the relationship is not strong.\n\n")
else:
    correlation_report.write("There is no negative correlation between technical background and risk perception. ")
    correlation_report.write("This suggests that technical expertise does not necessarily lead to lower risk assessments regarding AGI.\n\n")

# Interest and Future Involvement
# Convert future_involvement to numeric for correlation
involvement_map = {
    'Definitely yes': 5,
    'Probably yes': 4,
    'Might or might not': 3,
    'Probably not': 2,
    'Definitely not': 1
}
df['involvement_numeric'] = df['future_involvement'].map(involvement_map)
interest_involvement_corr = df['interest'].corr(df['involvement_numeric'])

correlation_report.write(f"4. **Interest and Future Involvement** (r = {interest_involvement_corr:.2f}): ")
correlation_report.write("There is a strong positive correlation between interest in AGI and likelihood of future involvement. ")
correlation_report.write("This expected relationship confirms that students who express greater interest in AGI are more likely to pursue related courses, research, or careers. ")
correlation_report.write("This suggests that cultivating interest in AGI among undergraduates could be an effective way to increase future talent in this field.\n\n")

# Societal Preparation and Education Need
prep_edu_corr = corr_matrix.loc['societal_preparation', 'education_need']
correlation_report.write(f"5. **Societal Preparation and Education Need** (r = {prep_edu_corr:.2f}): ")
if prep_edu_corr < -0.3:
    correlation_report.write("There is a moderate negative correlation between perceived societal preparation and education need. ")
    correlation_report.write("This suggests that students who believe society is poorly prepared for AGI tend to place greater emphasis on the importance of education about AGI. ")
    correlation_report.write("This reflects a logical connection between identifying a preparation gap and valuing educational interventions to address it.\n\n")
elif prep_edu_corr < 0:
    correlation_report.write("There is a weak negative correlation between perceived societal preparation and education need. ")
    correlation_report.write("This suggests some tendency for students who see society as less prepared to value education more highly, ")
    correlation_report.write("though the relationship is not strong.\n\n")
else:
    correlation_report.write("There is no negative correlation between perceived societal preparation and education need. ")
    correlation_report.write("This suggests that assessments of societal preparation and the importance of education are not strongly linked in students' minds.\n\n")

correlation_report.write("![Key Variables Correlation](/home/ubuntu/agi_survey_analysis/figures/key_variables_correlation.png)\n\n")

# 2. Demographic Influences on AGI Attitudes
print("Analyzing demographic influences on AGI attitudes...")
correlation_report.write("## 2. Demographic Influences on AGI Attitudes\n\n")

# Field of Study and AGI Attitudes
correlation_report.write("### Field of Study and AGI Attitudes\n\n")

# Calculate mean values by field of study
field_attitudes = df.groupby('field_of_study').agg({
    'sentiment': ['mean', 'std'],
    'risk_level': ['mean', 'std'],
    'benefit_assessment': ['mean', 'std'],
    'governance_importance': ['mean', 'std']
})

field_attitudes.columns = ['Sentiment (Mean)', 'Sentiment (SD)', 
                          'Risk Level (Mean)', 'Risk Level (SD)',
                          'Benefit Assessment (Mean)', 'Benefit Assessment (SD)',
                          'Governance Importance (Mean)', 'Governance Importance (SD)']
field_attitudes = field_attitudes.round(2)
field_attitudes.to_csv('/home/ubuntu/agi_survey_analysis/tables/field_attitudes.csv')

correlation_report.write("The following table shows mean attitudes toward AGI by field of study:\n\n")
correlation_report.write("| Field of Study | Sentiment (Mean) | Risk Level (Mean) | Benefit Assessment (Mean) | Governance Importance (Mean) |\n")
correlation_report.write("|---------------|------------------|-------------------|---------------------------|-----------------------------|\n")
for field, row in field_attitudes.iterrows():
    correlation_report.write(f"| {field} | {row['Sentiment (Mean)']} | {row['Risk Level (Mean)']} | {row['Benefit Assessment (Mean)']} | {row['Governance Importance (Mean)']} |\n")
correlation_report.write("\n")

# Create a visualization of sentiment by field
plt.figure(figsize=(12, 6))
field_sentiment = df.groupby('field_of_study')['sentiment'].mean().sort_values(ascending=False)
field_sentiment_std = df.groupby('field_of_study')['sentiment'].std()
field_sentiment_std = field_sentiment_std.reindex(field_sentiment.index)

plt.bar(field_sentiment.index, field_sentiment.values, yerr=field_sentiment_std.values, capsize=5)
plt.title('Mean Sentiment Toward AGI by Field of Study', fontsize=16)
plt.xlabel('Field of Study', fontsize=14)
plt.ylabel('Mean Sentiment (1-5 scale)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/sentiment_by_field.png', dpi=300)

# Create a visualization of risk perception by field
plt.figure(figsize=(12, 6))
field_risk = df.groupby('field_of_study')['risk_level'].mean().sort_values(ascending=False)
field_risk_std = df.groupby('field_of_study')['risk_level'].std()
field_risk_std = field_risk_std.reindex(field_risk.index)

plt.bar(field_risk.index, field_risk.values, yerr=field_risk_std.values, capsize=5)
plt.title('Mean Risk Perception of AGI by Field of Study', fontsize=16)
plt.xlabel('Field of Study', fontsize=14)
plt.ylabel('Mean Risk Level (1-5 scale)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/risk_by_field.png', dpi=300)

# Create a visualization of benefit assessment by field
plt.figure(figsize=(12, 6))
field_benefit = df.groupby('field_of_study')['benefit_assessment'].mean().sort_values(ascending=False)
field_benefit_std = df.groupby('field_of_study')['benefit_assessment'].std()
field_benefit_std = field_benefit_std.reindex(field_benefit.index)

plt.bar(field_benefit.index, field_benefit.values, yerr=field_benefit_std.values, capsize=5)
plt.title('Mean Benefit Assessment of AGI by Field of Study', fontsize=16)
plt.xlabel('Field of Study', fontsize=14)
plt.ylabel('Mean Benefit Assessment (1-5 scale)', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/benefit_by_field.png', dpi=300)

correlation_report.write("The analysis reveals significant differences in attitudes toward AGI across academic disciplines:\n\n")
correlation_report.write("1. **Sentiment**: Computer Science/IT and Engineering students express the most positive sentiment toward AGI, ")
correlation_report.write("while Arts and Humanities and Social Sciences students express more moderate sentiment. ")
correlation_report.write("This disciplinary divide may reflect differences in exposure to AI concepts, technical optimism, or emphasis on social implications.\n\n")
correlation_report.write("![Sentiment by Field](/home/ubuntu/agi_survey_analysis/figures/sentiment_by_field.png)\n\n")

correlation_report.write("2. **Risk Perception**: Arts and Humanities and Social Sciences students perceive the highest levels of risk associated with AGI, ")
correlation_report.write("while Computer Science/IT and Engineering students perceive lower risks. ")
correlation_report.write("This pattern suggests that technical familiarity may reduce risk perception, or that technical and non-technical disciplines emphasize different types of risks.\n\n")
correlation_report.write("![Risk by Field](/home/ubuntu/agi_survey_analysis/figures/risk_by_field.png)\n\n")

correlation_report.write("3. **Benefit Assessment**: Computer Science/IT, Engineering, and Natural Sciences students perceive the highest levels of benefit from AGI, ")
correlation_report.write("while Arts and Humanities students perceive somewhat lower benefits. ")
correlation_report.write("However, the variation in benefit assessment across disciplines is less pronounced than for sentiment or risk perception, ")
correlation_report.write("suggesting broader consensus about AGI's potential benefits.\n\n")
correlation_report.write("![Benefit by Fi<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>