import pandas as pd
import numpy as np
import random
import json
from datetime import datetime

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Load demographic profiles
profiles = pd.read_csv('/home/ubuntu/agi_survey_simulation/demographic_profiles.csv')
num_responses = len(profiles)

print(f"Loaded {num_responses} demographic profiles. Generating survey responses...")

# Initialize dataframe for survey responses
responses = pd.DataFrame()

# Copy demographic data to responses
for col in profiles.columns:
    responses[col] = profiles[col]

# Define AGI understanding responses based on AI familiarity
def generate_agi_understanding(familiarity, field):
    if familiarity == 1:
        templates = [
            "I think it's like robots that can think for themselves.",
            "AI that is smarter than humans, like in sci-fi movies.",
            "Computers that can do anything humans can do.",
            "I'm not really sure, but I think it's advanced AI.",
            "Robots that can make decisions on their own."
        ]
    elif familiarity == 2:
        templates = [
            "AI that can perform multiple tasks like humans, not just specific functions.",
            "Intelligence that can be applied to any problem, not just what it was programmed for.",
            "AI systems that can learn and adapt to new situations without being specifically programmed.",
            "Computer systems that can think and reason like humans across different domains.",
            "Advanced AI that can understand and learn from its environment."
        ]
    elif familiarity == 3:
        templates = [
            "AI systems that possess human-like general intelligence and can perform any intellectual task that a human can.",
            "Artificial intelligence that can understand, learn, and apply knowledge across different domains, similar to human intelligence.",
            "Systems that demonstrate intelligence across a wide range of cognitive tasks rather than specializing in one area.",
            "AI that can transfer knowledge between different domains and adapt to new problems without specific training.",
            "Machine intelligence that exhibits flexibility and adaptability across various cognitive tasks."
        ]
    elif familiarity == 4:
        templates = [
            "AGI refers to AI systems that possess the ability to understand, learn, and apply intelligence across multiple domains, similar to human general intelligence. Unlike narrow AI, AGI can transfer knowledge between domains and adapt to new situations.",
            "Artificial General Intelligence is the hypothetical ability of an AI system to understand, learn, and apply intelligence across a wide variety of tasks at a level equal to or exceeding human capabilities, without domain-specific training.",
            "AGI represents machine intelligence that can perform any intellectual task that a human can, with the ability to generalize learning across domains and demonstrate common sense reasoning.",
            "A form of artificial intelligence that would have the capacity to understand, learn, and apply knowledge across different domains with human-like flexibility, adaptability, and general problem-solving capabilities.",
            "AI systems that demonstrate human-equivalent intelligence across the full range of cognitive tasks, including reasoning, planning, learning, and adapting to new environments without specific programming."
        ]
    else:  # familiarity == 5
        templates = [
            "AGI refers to AI systems that possess human-equivalent or superior intelligence across all cognitive domains, characterized by the ability to generalize learning, transfer knowledge between domains, exhibit common sense reasoning, and adapt to novel situations without explicit programming or narrow specialization.",
            "Artificial General Intelligence represents a hypothetical form of machine intelligence with the capacity to understand, learn, and apply knowledge across any domain that a human can, while also possessing the ability to improve itself, reason abstractly, and potentially develop consciousness or self-awareness.",
            "AGI is defined as machine intelligence that matches or exceeds human cognitive abilities across all relevant domains, including but not limited to: abstract reasoning, natural language understanding, learning from limited examples, adapting to new environments, and exhibiting general problem-solving capabilities without domain-specific training.",
            "A form of artificial intelligence that demonstrates human-level competence across the full spectrum of cognitive tasks, characterized by robust transfer learning, meta-learning capabilities, causal reasoning, and the ability to operate effectively in open-ended, uncertain environments without task-specific optimization.",
            "AGI represents the theoretical point at which machine intelligence achieves human-equivalent general intelligence, including capabilities for abstract reasoning, transfer learning, common sense understanding, and autonomous improvement, potentially leading to recursive self-improvement and superintelligence."
        ]
    
    # Adjust based on field of study
    if field in ["Computer Science/IT", "Engineering"]:
        # More technical language
        technical_adjustment = random.choice([
            " This would require advanced neural architectures, possibly with attention mechanisms and meta-learning capabilities.",
            " Current approaches like large language models show promising capabilities but lack true understanding and reasoning.",
            " This differs from narrow AI systems that excel only at specific tasks they were trained for.",
            " The path to AGI might involve integrating symbolic reasoning with deep learning approaches.",
            " This represents a significant challenge in computer science and AI research."
        ])
        
        # Add technical adjustment to responses for technical fields
        if familiarity >= 3:
            selected_template = random.choice(templates) + technical_adjustment
        else:
            selected_template = random.choice(templates)
            
    elif field in ["Philosophy", "Social Sciences"]:
        # More philosophical/ethical considerations
        philosophical_adjustment = random.choice([
            " This raises important ethical questions about consciousness, rights, and humanity's future.",
            " The development of such systems would have profound implications for society, labor, and human identity.",
            " This concept challenges our understanding of what intelligence and consciousness truly are.",
            " The philosophical implications of creating such intelligence are vast and largely unexplored.",
            " This represents a fundamental shift in humanity's relationship with technology and possibly our role in the universe."
        ])
        
        # Add philosophical adjustment to responses for humanities/social science fields
        if familiarity >= 3:
            selected_template = random.choice(templates) + philosophical_adjustment
        else:
            selected_template = random.choice(templates)
    else:
        selected_template = random.choice(templates)
    
    return selected_template

# Generate AGI understanding responses
responses['agi_understanding'] = responses.apply(
    lambda row: generate_agi_understanding(row['ai_familiarity'], row['field_of_study']), 
    axis=1
)

# Generate AGI timeline responses
def generate_agi_timeline(familiarity, field, technical_bg):
    # Base probabilities
    if field in ["Computer Science/IT", "Engineering"] and technical_bg >= 4:
        # Technical experts tend to have longer timelines
        probs = [0.01, 0.10, 0.35, 0.40, 0.10, 0.04]
    elif field in ["Computer Science/IT", "Engineering"]:
        # Technical fields but not experts
        probs = [0.02, 0.15, 0.40, 0.30, 0.10, 0.03]
    elif familiarity >= 4:
        # High familiarity non-technical
        probs = [0.03, 0.20, 0.35, 0.25, 0.12, 0.05]
    elif familiarity >= 3:
        # Medium familiarity
        probs = [0.05, 0.25, 0.35, 0.20, 0.10, 0.05]
    else:
        # Low familiarity - more varied and potentially shorter timelines
        probs = [0.10, 0.30, 0.25, 0.15, 0.15, 0.05]
    
    # Timeline options
    options = [
        "It already exists",
        "Within the next 10 years",
        "Within 10-25 years",
        "Within 25-50 years",
        "Within 50-100 years",
        "More than 100 years from now",
        "Never"
    ]
    
    # Add small probability for "Never" option
    never_prob = 0.025  # Fixed probability for "Never"
    remaining_prob = 1.0 - never_prob
    
    # Normalize the first 6 probabilities to sum to remaining_prob
    current_sum = sum(probs)
    normalized_probs = [p * (remaining_prob / current_sum) for p in probs]
    
    # Add the "Never" probability
    normalized_probs.append(never_prob)
    
    # Verify probabilities sum to 1
    assert abs(sum(normalized_probs) - 1.0) < 1e-10, "Probabilities must sum to 1"
    
    return np.random.choice(options, p=normalized_probs)

responses['agi_timeline'] = responses.apply(
    lambda row: generate_agi_timeline(
        row['ai_familiarity'], 
        row['field_of_study'], 
        row['technical_background']
    ), 
    axis=1
)

# Generate sentiment toward AGI
def generate_sentiment(familiarity, field, technical_bg):
    # Base sentiment distribution (slightly positive overall)
    base_mean = 3.3
    base_std = 1.0
    
    # Adjust based on field and background
    if field in ["Computer Science/IT", "Engineering"]:
        field_adjustment = 0.3  # More positive
    elif field in ["Arts and Humanities"]:
        field_adjustment = -0.2  # More cautious
    else:
        field_adjustment = 0
    
    # Technical background adjustment
    tech_adjustment = (technical_bg - 3) * 0.1
    
    # Familiarity adjustment (more familiar = slightly more positive)
    familiarity_adjustment = (familiarity - 3) * 0.1
    
    # Calculate adjusted mean
    adjusted_mean = base_mean + field_adjustment + tech_adjustment + familiarity_adjustment
    
    # Generate sentiment score (1-5)
    sentiment = round(np.random.normal(adjusted_mean, base_std))
    
    # Ensure within bounds
    return max(1, min(5, sentiment))

responses['sentiment'] = responses.apply(
    lambda row: generate_sentiment(
        row['ai_familiarity'], 
        row['field_of_study'], 
        row['technical_background']
    ), 
    axis=1
)

# Generate interest level
def generate_interest(familiarity, sentiment):
    # Base interest is correlated with familiarity
    base_interest = familiarity
    
    # Adjust based on sentiment (more positive = more interested)
    sentiment_adjustment = (sentiment - 3) * 0.5
    
    # Calculate adjusted interest
    adjusted_interest = base_interest + sentiment_adjustment
    
    # Add some noise
    interest = round(adjusted_interest + np.random.normal(0, 0.5))
    
    # Ensure within bounds
    return max(1, min(5, interest))

responses['interest'] = responses.apply(
    lambda row: generate_interest(row['ai_familiarity'], row['sentiment']), 
    axis=1
)

# Generate application likelihood grid
def generate_applications_grid(familiarity, field, technical_bg):
    # Areas to rate
    areas = [
        'Education', 
        'Healthcare', 
        'Scientific research', 
        'Entertainment', 
        'Personal assistance', 
        'Business/finance', 
        'Military/defense'
    ]
    
    # Base likelihoods (slightly optimistic overall)
    base_likelihoods = {
        'Education': 4,
        'Healthcare': 4,
        'Scientific research': 4.5,
        'Entertainment': 3.5,
        'Personal assistance': 4,
        'Business/finance': 4,
        'Military/defense': 3.5
    }
    
    # Field-specific adjustments
    field_adjustments = {
        'Education': 0.5 if field == 'Education' else 0,
        'Healthcare': 0.5 if field == 'Health Sciences' else 0,
        'Scientific research': 0.5 if field in ['Natural Sciences', 'Computer Science/IT'] else 0,
        'Entertainment': 0.5 if field == 'Arts and Humanities' else 0,
        'Business/finance': 0.5 if field == 'Business/Economics' else 0,
        'Military/defense': 0.3 if field == 'Engineering' else 0
    }
    
    # Generate ratings for each area
    ratings = {}
    for area in areas:
        # Base rating
        base = base_likelihoods.get(area, 3.5)
        
        # Field adjustment
        field_adj = field_adjustments.get(area, 0)
        
        # Familiarity adjustment (more familiar = more nuanced/realistic expectations)
        familiarity_adj = (familiarity - 3) * 0.1
        
        # Calculate mean rating
        mean_rating = base + field_adj + familiarity_adj
        
        # Add noise
        rating = round(np.random.normal(mean_rating, 0.7))
        
        # Ensure within bounds (1-5)
        rating = max(1, min(5, rating))
        
        # Convert to text rating
        rating_map = {
            1: 'Very unlikely',
            2: 'Unlikely',
            3: 'Neutral',
            4: 'Likely',
            5: 'Very likely'
        }
        
        ratings[area] = rating_map[rating]
    
    return ratings

# Generate application grid responses
responses['applications_grid'] = responses.apply(
    lambda row: generate_applications_grid(
        row['ai_familiarity'], 
        row['field_of_study'], 
        row['technical_background']
    ), 
    axis=1
)

# Generate personal use responses
def generate_personal_use(familiarity, field, interest):
    if interest <= 2:  # Low interest
        templates = [
            "I'm not sure I would use it personally.",
            "I don't think I would use it much in my daily life.",
            "I might try it out of curiosity, but I don't see regular use for it.",
            "I would probably be cautious about using it.",
            "I don't see many personal applications for it right now."
        ]
    elif interest == 3:  # Moderate interest
        templates = [
            "I would use it to help with everyday tasks like organizing my schedule and finding information.",
            "I could see using it for research and learning new topics more efficiently.",
            "It might be helpful for creative projects and generating ideas.",
            "I would use it to automate routine tasks and save time.",
            "I'd probably use it for both work and personal projects to increase productivity."
        ]
    else:  # High interest
        templates = [
            "I would integrate it into many aspects of my life - from academic research to creative projects, personal organization, and learning new skills.",
            "I'd use it extensively for my studies, career development, creative endeavors, and to optimize my daily routines and decision-making.",
            "I would leverage it to enhance my learning, automate routine tasks, assist with complex problem-solving, and explore new ideas and possibilities.",
            "I'd use it as a personal assistant, research partner, creative collaborator, and learning tool to dramatically expand my capabilities.",
            "I would use it to accelerate my learning, improve my productivity, enhance my creative work, and help make better decisions in both personal and professional contexts."
        ]
    
    # Field-specific additions
    field_additions = {
        'Computer Science/IT': [
            "I would use it to help debug code and learn new programming languages.",
            "It would be useful for generating code snippets and explaining complex algorithms.",
            "I could use it to help design and optimize software systems.",
            "It would be valuable for stayi<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>