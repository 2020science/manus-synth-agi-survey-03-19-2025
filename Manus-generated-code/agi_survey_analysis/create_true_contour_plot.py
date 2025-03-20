import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['font.size'] = 14

# Create a contour plot (not KDE) with labeled contours
plt.figure(figsize=(12, 10))

# Create a 2D histogram first to understand the data distribution
hist, xedges, yedges = np.histogram2d(df['risk_level'], df['benefit_assessment'], 
                                     bins=[5, 5], range=[[0.5, 5.5], [0.5, 5.5]])

# Create a meshgrid for contour plotting
x_centers = (xedges[:-1] + xedges[1:]) / 2
y_centers = (yedges[:-1] + yedges[1:]) / 2
X, Y = np.meshgrid(x_centers, y_centers)

# Transpose the histogram to match the meshgrid orientation
Z = hist.T

# Create a filled contour plot
contourf = plt.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
plt.colorbar(contourf, label='Number of Respondents')

# Add labeled contour lines
contour = plt.contour(X, Y, Z, levels=8, colors='white', alpha=0.7, linewidths=1.5)
plt.clabel(contour, inline=True, fontsize=10, fmt='%d', colors='white')

# Add scatter plot with transparency to show individual data points
plt.scatter(df['risk_level'], df['benefit_assessment'], alpha=0.1, color='white', edgecolor='gray')

# Add a diagonal line for reference (risk = benefit)
plt.plot([1, 5], [1, 5], 'k--', alpha=0.3)

# Add quadrant dividing lines
plt.axvline(x=3, color='white', linestyle='--', alpha=0.5)
plt.axhline(y=3, color='white', linestyle='--', alpha=0.5)

# Add text annotations for quadrants with improved visibility (without percentages)
# Create a function to add text with background
def add_text_with_background(x, y, text, fontsize=14, ha='center', va='center', bg_color='black', text_color='white', alpha=0.7):
    text_obj = plt.text(x, y, text, fontsize=fontsize, ha=ha, va=va, color=text_color, 
                        bbox=dict(facecolor=bg_color, alpha=alpha, edgecolor='none', boxstyle='round,pad=0.5'))
    return text_obj

# Add quadrant labels with backgrounds
add_text_with_background(1.5, 4.5, 'High Benefit, Low Risk\n(Techno-optimists)', fontsize=14)
add_text_with_background(4.5, 4.5, 'High Benefit, High Risk\n(Cautious optimists)', fontsize=14)
add_text_with_background(1.5, 1.5, 'Low Benefit, Low Risk\n(Disinterested)', fontsize=14)
add_text_with_background(4.5, 1.5, 'Low Benefit, High Risk\n(Techno-pessimists)', fontsize=14)

# Set labels and title
plt.title('Risk vs. Benefit Assessment of AGI Among Undergraduate Students\n(Contour Plot with Labeled Contours)', fontsize=18)
plt.xlabel('Risk Level (1=Very low risk, 5=Very high risk)', fontsize=16)
plt.ylabel('Benefit Level (1=Very low benefit, 5=Very high benefit)', fontsize=16)
plt.xticks(range(1, 6), fontsize=14)
plt.yticks(range(1, 6), fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)

# Set axis limits
plt.xlim(0.5, 5.5)
plt.ylim(0.5, 5.5)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/risk_benefit_true_contour_labeled.png', dpi=300)
print("True contour plot with labeled contours created and saved to /home/ubuntu/agi_survey_analysis/figures/risk_benefit_true_contour_labeled.png")
