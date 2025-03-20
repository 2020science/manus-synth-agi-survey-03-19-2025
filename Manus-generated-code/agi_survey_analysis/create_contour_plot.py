import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['font.size'] = 14

# Create a contour plot of risk vs. benefit
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

# Create a contour plot
contour = plt.contourf(X, Y, Z, levels=20, cmap='viridis', alpha=0.8)
plt.colorbar(contour, label='Number of Respondents')

# Add scatter plot with transparency to show individual data points
plt.scatter(df['risk_level'], df['benefit_assessment'], alpha=0.1, color='white', edgecolor='gray')

# Add a diagonal line for reference (risk = benefit)
plt.plot([1, 5], [1, 5], 'k--', alpha=0.3)

# Add text annotations for quadrants
plt.text(1.5, 4.5, 'High Benefit, Low Risk\n(Techno-optimists)', fontsize=14, ha='center', color='white')
plt.text(4.5, 4.5, 'High Benefit, High Risk\n(Cautious optimists)', fontsize=14, ha='center', color='white')
plt.text(1.5, 1.5, 'Low Benefit, Low Risk\n(Disinterested)', fontsize=14, ha='center', color='white')
plt.text(4.5, 1.5, 'Low Benefit, High Risk\n(Techno-pessimists)', fontsize=14, ha='center', color='white')

# Calculate percentages in each quadrant
high_risk = df['risk_level'] >= 4
low_risk = df['risk_level'] <= 2
high_benefit = df['benefit_assessment'] >= 4
low_benefit = df['benefit_assessment'] <= 2

techno_optimists = (low_risk & high_benefit).mean() * 100
cautious_optimists = (high_risk & high_benefit).mean() * 100
disinterested = (low_risk & low_benefit).mean() * 100
techno_pessimists = (high_risk & low_benefit).mean() * 100

# Add percentage annotations to each quadrant
plt.text(1.5, 4.0, f'{techno_optimists:.1f}% of respondents', fontsize=12, ha='center', color='white')
plt.text(4.5, 4.0, f'{cautious_optimists:.1f}% of respondents', fontsize=12, ha='center', color='white')
plt.text(1.5, 1.0, f'{disinterested:.1f}% of respondents', fontsize=12, ha='center', color='white')
plt.text(4.5, 1.0, f'{techno_pessimists:.1f}% of respondents', fontsize=12, ha='center', color='white')

# Set labels and title
plt.title('Risk vs. Benefit Assessment of AGI Among Undergraduate Students\n(Contour Plot Showing Response Density)', fontsize=18)
plt.xlabel('Risk Level (1=Very low risk, 5=Very high risk)', fontsize=16)
plt.ylabel('Benefit Level (1=Very low benefit, 5=Very high benefit)', fontsize=16)
plt.xticks(range(1, 6), fontsize=14)
plt.yticks(range(1, 6), fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)

# Set axis limits
plt.xlim(0.5, 5.5)
plt.ylim(0.5, 5.5)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/risk_benefit_contour_plot.png', dpi=300)
print("Contour plot created and saved to /home/ubuntu/agi_survey_analysis/figures/risk_benefit_contour_plot.png")

# Create a second version with kernel density estimation for smoother contours
plt.figure(figsize=(12, 10))

# Add some jitter to the data to better visualize the density
x = df['risk_level'] + np.random.normal(0, 0.1, len(df))
y = df['benefit_assessment'] + np.random.normal(0, 0.1, len(df))

# Calculate the point density
xy = np.vstack([x, y])
z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = x[idx], y[idx], z[idx]

# Create a scatter plot colored by density
plt.scatter(x, y, c=z, s=50, alpha=0.6, cmap='viridis', edgecolor='none')
plt.colorbar(label='Density of Responses')

# Add contour lines to show density regions
k = gaussian_kde(np.vstack([df['risk_level'], df['benefit_assessment']]))
xi, yi = np.mgrid[0.5:5.5:100j, 0.5:5.5:100j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))
zi = zi.reshape(xi.shape)
plt.contour(xi, yi, zi, levels=5, colors='white', alpha=0.5, linewidths=1)

# Add a diagonal line for reference (risk = benefit)
plt.plot([1, 5], [1, 5], 'k--', alpha=0.3)

# Add text annotations for quadrants
plt.text(1.5, 4.5, 'High Benefit, Low Risk\n(Techno-optimists)', fontsize=14, ha='center', color='white')
plt.text(4.5, 4.5, 'High Benefit, High Risk\n(Cautious optimists)', fontsize=14, ha='center', color='white')
plt.text(1.5, 1.5, 'Low Benefit, Low Risk\n(Disinterested)', fontsize=14, ha='center', color='white')
plt.text(4.5, 1.5, 'Low Benefit, High Risk\n(Techno-pessimists)', fontsize=14, ha='center', color='white')

# Add percentage annotations to each quadrant
plt.text(1.5, 4.0, f'{techno_optimists:.1f}% of respondents', fontsize=12, ha='center', color='white')
plt.text(4.5, 4.0, f'{cautious_optimists:.1f}% of respondents', fontsize=12, ha='center', color='white')
plt.text(1.5, 1.0, f'{disinterested:.1f}% of respondents', fontsize=12, ha='center', color='white')
plt.text(4.5, 1.0, f'{techno_pessimists:.1f}% of respondents', fontsize=12, ha='center', color='white')

# Set labels and title
plt.title('Risk vs. Benefit Assessment of AGI Among Undergraduate Students\n(Kernel Density Estimation)', fontsize=18)
plt.xlabel('Risk Level (1=Very low risk, 5=Very high risk)', fontsize=16)
plt.ylabel('Benefit Level (1=Very low benefit, 5=Very high benefit)', fontsize=16)
plt.xticks(range(1, 6), fontsize=14)
plt.yticks(range(1, 6), fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)

# Set axis limits
plt.xlim(0.5, 5.5)
plt.ylim(0.5, 5.5)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/risk_benefit_kde_plot.png', dpi=300)
print("KDE plot created and saved to /home/ubuntu/agi_survey_analysis/figures/risk_benefit_kde_plot.png")
