import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.patches import Rectangle

# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")
plt.rcParams['figure.figsize'] = (12, 10)
plt.rcParams['font.size'] = 14

# Create a KDE plot with improved quadrant labels but no percentages
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
scatter = plt.scatter(x, y, c=z, s=50, alpha=0.6, cmap='viridis', edgecolor='none')
plt.colorbar(scatter, label='Density of Responses')

# Add contour lines to show density regions with labels
k = gaussian_kde(np.vstack([df['risk_level'], df['benefit_assessment']]))
xi, yi = np.mgrid[0.5:5.5:100j, 0.5:5.5:100j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))
zi = zi.reshape(xi.shape)

# Create labeled contours
contour = plt.contour(xi, yi, zi, levels=5, colors='white', alpha=0.7, linewidths=1.5)
plt.clabel(contour, inline=True, fontsize=10, fmt='%.2f', colors='white')

# Add a diagonal line for reference (risk = benefit)
plt.plot([1, 5], [1, 5], 'k--', alpha=0.3)

# Add semi-transparent rectangles to highlight quadrants
# Techno-optimists (High Benefit, Low Risk)
plt.gca().add_patch(Rectangle((0.5, 3.5), 2, 2, alpha=0.1, color='lime', zorder=0))
# Cautious optimists (High Benefit, High Risk)
plt.gca().add_patch(Rectangle((3.5, 3.5), 2, 2, alpha=0.1, color='yellow', zorder=0))
# Disinterested (Low Benefit, Low Risk)
plt.gca().add_patch(Rectangle((0.5, 0.5), 2, 2, alpha=0.1, color='lightblue', zorder=0))
# Techno-pessimists (Low Benefit, High Risk)
plt.gca().add_patch(Rectangle((3.5, 0.5), 2, 2, alpha=0.1, color='red', zorder=0))

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
plt.title('Risk vs. Benefit Assessment of AGI Among Undergraduate Students\n(Kernel Density Estimation with Labeled Contours)', fontsize=18)
plt.xlabel('Risk Level (1=Very low risk, 5=Very high risk)', fontsize=16)
plt.ylabel('Benefit Level (1=Very low benefit, 5=Very high benefit)', fontsize=16)
plt.xticks(range(1, 6), fontsize=14)
plt.yticks(range(1, 6), fontsize=14)
plt.grid(True, linestyle='--', alpha=0.3)

# Set axis limits
plt.xlim(0.5, 5.5)
plt.ylim(0.5, 5.5)

plt.tight_layout()
plt.savefig('/home/ubuntu/agi_survey_analysis/figures/risk_benefit_contour_labeled.png', dpi=300)
print("Contour plot with labeled contours created and saved to /home/ubuntu/agi_survey_analysis/figures/risk_benefit_contour_labeled.png")
