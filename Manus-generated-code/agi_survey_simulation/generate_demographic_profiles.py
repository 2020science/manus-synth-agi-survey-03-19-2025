import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of simulated responses
num_responses = 1000

# Create empty dataframe to store demographic profiles
profiles = pd.DataFrame()

# Generate age distribution
age_categories = ['18-19', '20-21', '22-23', '24-25', '26+']
age_probabilities = [0.30, 0.35, 0.25, 0.07, 0.03]
profiles['age'] = np.random.choice(age_categories, size=num_responses, p=age_probabilities)

# Generate gender distribution
gender_categories = ['Male', 'Female', 'Non-binary/third gender', 'Prefer to self-describe', 'Prefer not to say']
gender_probabilities = [0.48, 0.48, 0.03, 0.005, 0.005]
profiles['gender'] = np.random.choice(gender_categories, size=num_responses, p=gender_probabilities)

# Generate academic year distribution
year_categories = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Other']
year_probabilities = [0.27, 0.25, 0.24, 0.22, 0.02]

# Initialize academic year column
profiles['academic_year'] = ''

# Apply correlation between age and academic year
for i in range(num_responses):
    age = profiles.loc[i, 'age']
    if age == '18-19':
        year_probs = [0.85, 0.10, 0.03, 0.01, 0.01]
    elif age == '20-21':
        year_probs = [0.10, 0.45, 0.35, 0.09, 0.01]
    elif age == '22-23':
        year_probs = [0.03, 0.15, 0.42, 0.38, 0.02]
    elif age == '24-25':
        year_probs = [0.02, 0.08, 0.20, 0.65, 0.05]
    else:  # 26+
        year_probs = [0.05, 0.10, 0.15, 0.60, 0.10]
    
    profiles.loc[i, 'academic_year'] = np.random.choice(year_categories, p=year_probs)

# Generate field of study distribution
field_categories = [
    'Arts and Humanities', 
    'Social Sciences', 
    'Business/Economics', 
    'Natural Sciences', 
    'Computer Science/IT', 
    'Engineering', 
    'Health Sciences', 
    'Education', 
    'Other'
]
field_probabilities = [0.15, 0.20, 0.15, 0.15, 0.10, 0.12, 0.08, 0.04, 0.01]
profiles['field_of_study'] = np.random.choice(field_categories, size=num_responses, p=field_probabilities)

# Initialize AI familiarity and technical background columns
profiles['ai_familiarity'] = 0
profiles['technical_background'] = 0

# Apply correlation between field of study and technical background/AI familiarity
for i in range(num_responses):
    field = profiles.loc[i, 'field_of_study']
    
    # Set technical background based on field of study
    if field in ['Computer Science/IT', 'Engineering']:
        tech_probs = [0.05, 0.10, 0.25, 0.35, 0.25]
    elif field in ['Natural Sciences', 'Business/Economics']:
        tech_probs = [0.10, 0.25, 0.35, 0.20, 0.10]
    elif field in ['Health Sciences']:
        tech_probs = [0.15, 0.30, 0.35, 0.15, 0.05]
    elif field in ['Social Sciences', 'Education']:
        tech_probs = [0.25, 0.35, 0.25, 0.10, 0.05]
    else:  # Arts and Humanities, Other
        tech_probs = [0.35, 0.35, 0.20, 0.08, 0.02]
    
    profiles.loc[i, 'technical_background'] = np.random.choice([1, 2, 3, 4, 5], p=tech_probs)
    
    # Set AI familiarity based on field of study and technical background
    tech_bg = profiles.loc[i, 'technical_background']
    
    if field in ['Computer Science/IT', 'Engineering']:
        # Higher base familiarity for CS/Engineering
        base_familiarity = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.15, 0.30, 0.35, 0.15])
    elif field in ['Natural Sciences', 'Business/Economics']:
        base_familiarity = np.random.choice([1, 2, 3, 4, 5], p=[0.10, 0.25, 0.35, 0.25, 0.05])
    else:
        base_familiarity = np.random.choice([1, 2, 3, 4, 5], p=[0.20, 0.35, 0.30, 0.10, 0.05])
    
    # Adjust familiarity based on technical background
    adjustment = min(max(tech_bg - 3, -1), 1)  # Limit adjustment to +/- 1
    familiarity = min(max(base_familiarity + adjustment, 1), 5)  # Keep within 1-5 range
    
    profiles.loc[i, 'ai_familiarity'] = familiarity

# Generate information sources (multiple selection)
info_sources = [
    'Academic courses',
    'Scientific publications',
    'News media',
    'Social media',
    'Movies/TV shows',
    'Friends/family',
    "I don't follow AI developments"
]

# Initialize columns for each information source
for source in info_sources:
    column_name = 'info_' + source.replace("/", "_").replace(" ", "_").replace("'", "")
    profiles[column_name] = 0

# Apply correlation between AI familiarity and information sources
for i in range(num_responses):
    familiarity = profiles.loc[i, 'ai_familiarity']
    
    # Determine number of sources based on familiarity
    if familiarity == 1:
        num_sources = np.random.choice([0, 1, 2], p=[0.20, 0.50, 0.30])
    elif familiarity == 2:
        num_sources = np.random.choice([1, 2, 3], p=[0.30, 0.50, 0.20])
    elif familiarity == 3:
        num_sources = np.random.choice([1, 2, 3, 4], p=[0.10, 0.30, 0.40, 0.20])
    elif familiarity == 4:
        num_sources = np.random.choice([2, 3, 4, 5], p=[0.10, 0.30, 0.40, 0.20])
    else:  # familiarity == 5
        num_sources = np.random.choice([3, 4, 5, 6], p=[0.10, 0.30, 0.40, 0.20])
    
    # Special case for "I don't follow AI developments"
    if familiarity <= 2 and random.random() < 0.25:
        column_name = 'info_' + "I don't follow AI developments".replace("/", "_").replace(" ", "_").replace("'", "")
        profiles.loc[i, column_name] = 1
        # If they don't follow AI, reduce other sources
        if num_sources > 0:
            num_sources = max(0, num_sources - 1)
    
    # Select random sources
    if num_sources > 0:
        # Exclude "I don't follow AI developments" from regular selection
        available_sources = info_sources[:-1]
        
        # Probability adjustments based on familiarity
        if familiarity >= 4:  # High familiarity
            # Higher chance of academic and scientific sources
            source_probs = [0.25, 0.20, 0.15, 0.15, 0.10, 0.15]
        elif familiarity >= 3:  # Medium familiarity
            source_probs = [0.15, 0.10, 0.25, 0.25, 0.15, 0.10]
        else:  # Low familiarity
            # Higher chance of social media and entertainment
            source_probs = [0.05, 0.05, 0.20, 0.35, 0.25, 0.10]
        
        # Select sources based on probabilities
        selected_indices = np.random.choice(
            range(len(available_sources)), 
            size=min(num_sources, len(available_sources)), 
            p=source_probs, 
            replace=False
        )
        
        for idx in selected_indices:
            source = available_sources[idx]
            column_name = 'info_' + source.replace("/", "_").replace(" ", "_").replace("'", "")
            profiles.loc[i, column_name] = 1

# Save demographic profiles to CSV
profiles.to_csv('/home/ubuntu/agi_survey_simulation/demographic_profiles.csv', index=False)

print(f"Generated {num_responses} demographic profiles with realistic distributions and correlations.")
print(f"Data saved to /home/ubuntu/agi_survey_simulation/demographic_profiles.csv")

# Display summary statistics
print("\nSummary Statistics:")
print(f"Age distribution:\n{profiles['age'].value_counts(normalize=True).sort_index()}")
print(f"\nGender distribution:\n{profiles['gender'].value_counts(normalize=True)}")
print(f"\nAcademic year distribution:\n{profiles['academic_year'].value_counts(normalize=True)}")
print(f"\nField of study distribution:\n{profiles['field_of_study'].value_counts(normalize=True).sort_index()}")
print(f"\nAI familiarity distribution:\n{profiles['ai_familiarity'].value_counts(normalize=True).sort_index()}")
print(f"\nTechnical background distribution:\n{profiles['technical_background'].value_counts(normalize=True).sort_index()}")

# Information sources summary
print("\nInformation sources distribution:")
for source in info_sources:
    col_name = 'info_' + source.replace("/", "_").replace(" ", "_").replace("'", "")
    percentage = profiles[col_name].mean() * 100
    print(f"{source}: {percentage:.1f}%")
