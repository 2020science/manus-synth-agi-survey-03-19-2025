import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.patches import Rectangle

# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Print the actual percentages calculated from the data
high_risk = df['risk_level'] >= 4
low_risk = df['risk_level'] <= 2
high_benefit = df['benefit_assessment'] >= 4
low_benefit = df['benefit_assessment'] <= 2

techno_optimists = (low_risk & high_benefit).mean() * 100
cautious_optimists = (high_risk & high_benefit).mean() * 100
disinterested = (low_risk & low_benefit).mean() * 100
techno_pessimists = (high_risk & low_benefit).mean() * 100

print(f"Techno-optimists (High Benefit, Low Risk): {techno_optimists:.1f}%")
print(f"Cautious optimists (High Benefit, High Risk): {cautious_optimists:.1f}%")
print(f"Disinterested (Low Benefit, Low Risk): {disinterested:.1f}%")
print(f"Techno-pessimists (Low Benefit, High Risk): {techno_pessimists:.1f}%")

# Count the actual number of respondents in each quadrant
print("\nCounts in each quadrant:")
print(f"Techno-optimists (High Benefit, Low Risk): {(low_risk & high_benefit).sum()}")
print(f"Cautious optimists (High Benefit, High Risk): {(high_risk & high_benefit).sum()}")
print(f"Disinterested (Low Benefit, Low Risk): {(low_risk & low_benefit).sum()}")
print(f"Techno-pessimists (Low Benefit, High Risk): {(high_risk & low_benefit).sum()}")
print(f"Total respondents: {len(df)}")

# Check the distribution of risk and benefit values
print("\nRisk level distribution:")
print(df['risk_level'].value_counts().sort_index())

print("\nBenefit assessment distribution:")
print(df['benefit_assessment'].value_counts().sort_index())

# Check the distribution of combinations
print("\nCombinations of risk and benefit:")
combo_counts = df.groupby(['risk_level', 'benefit_assessment']).size().reset_index(name='count')
print(combo_counts.sort_values(['risk_level', 'benefit_assessment']))
