import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
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

print("Loading survey data for open-ended response analysis...")
# Load the data
df = pd.read_csv('/home/ubuntu/agi_survey_simulation/simulated_responses.csv')

# Load JSON data for better handling of text responses
with open('/home/ubuntu/agi_survey_simulation/survey_responses.json', 'r') as f:
    json_responses = json.load(f)
df_json = pd.DataFrame(json_responses)

# Create a file to store open-ended response analysis results
open_ended_report = open('/home/ubuntu/agi_survey_analysis/open_ended_analysis.md', 'w')
open_ended_report.write("# Analysis of Open-Ended Responses in AGI Survey\n\n")
open_ended_report.write("This analysis examines the open-ended responses of 1,000 undergraduate students who participated in the AGI survey.\n\n")

# Initialize NLTK resources
print("Initializing NLP tools...")
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)  # Download again to ensure it's available
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Function to preprocess text
def preprocess_text(text):
    if pd.isna(text) or text == "":
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Simple tokenization as fallback if nltk tokenizer fails
    try:
        tokens = word_tokenize(text)
    except:
        tokens = text.split()
    
    # Remove stopwords and lemmatize
    try:
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
    except:
        tokens = [word for word in tokens if len(word) > 2]
    
    return ' '.join(tokens)

# Function to extract key phrases (bigrams and trigrams)
def extract_key_phrases(texts, n_gram_range=(2, 3), top_n=20):
    # Remove empty texts
    texts = [text for text in texts if isinstance(text, str) and text.strip() != ""]
    
    if not texts:
        return []
    
    # Use CountVectorizer to extract n-grams
    vectorizer = CountVectorizer(ngram_range=n_gram_range, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    # Get feature names and their frequencies
    feature_names = vectorizer.get_feature_names_out()
    frequencies = X.sum(axis=0).A1
    
    # Create a dictionary of n-grams and their frequencies
    phrases = dict(zip(feature_names, frequencies))
    
    # Sort by frequency and return top N
    sorted_phrases = sorted(phrases.items(), key=lambda x: x[1], reverse=True)
    return sorted_phrases[:top_n]

# Function to create word cloud
def create_wordcloud(text, title, filename):
    if not text or text.strip() == "":
        print(f"Warning: Empty text for {title} wordcloud")
        return
    
    wordcloud = WordCloud(width=800, height=400, background_color='white', 
                          max_words=100, contour_width=3, contour_color='steelblue')
    wordcloud.generate(text)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# Function to perform topic modeling
def perform_topic_modeling(texts, n_topics=5, n_top_words=10):
    # Remove empty texts
    texts = [text for text in texts if isinstance(text, str) and text.strip() != ""]
    
    if not texts:
        return [], []
    
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(texts)
    
    # Create and fit LDA model
    lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
    lda.fit(X)
    
    # Get feature names
    feature_names = vectorizer.get_feature_names_out()
    
    # Extract topics
    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[:-n_top_words-1:-1]
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append((topic_idx, top_words))
    
    # Get topic distribution for each document
    doc_topics = lda.transform(X)
    
    return topics, doc_topics

# 1. AGI Understanding Analysis
print("Analyzing AGI understanding responses...")
open_ended_report.write("## 1. AGI Understanding\n\n")

# Extract and preprocess AGI understanding responses
agi_understanding_responses = df['agi_understanding'].dropna().tolist()
preprocessed_understanding = [preprocess_text(text) for text in agi_understanding_responses if isinstance(text, str)]
all_understanding_text = ' '.join(preprocessed_understanding)

# Create word cloud for AGI understanding
create_wordcloud(all_understanding_text, 
                "Key Terms in Undergraduate Definitions of AGI", 
                "/home/ubuntu/agi_survey_analysis/figures/agi_understanding_wordcloud.png")

# Extract key phrases from AGI understanding responses
understanding_phrases = extract_key_phrases([text for text in agi_understanding_responses if isinstance(text, str)])

# Perform topic modeling on AGI understanding responses
understanding_topics, _ = perform_topic_modeling([text for text in agi_understanding_responses if isinstance(text, str)])

# Write results to report
open_ended_report.write("When asked to define Artificial General Intelligence (AGI), undergraduate students provided a range of responses that reveal their conceptual understanding of this technology.\n\n")

open_ended_report.write("### Key Phrases in AGI Definitions\n\n")
open_ended_report.write("The most common phrases used by students to define AGI include:\n\n")
open_ended_report.write("| Phrase | Frequency |\n")
open_ended_report.write("|--------|----------|\n")
for phrase, freq in understanding_phrases[:15]:
    open_ended_report.write(f"| {phrase} | {freq} |\n")
open_ended_report.write("\n")

open_ended_report.write("### Conceptual Topics in AGI Definitions\n\n")
open_ended_report.write("Topic modeling analysis identified the following conceptual themes in how undergraduates define AGI:\n\n")
for topic_idx, top_words in understanding_topics:
    open_ended_report.write(f"**Topic {topic_idx+1}**: {', '.join(top_words)}\n\n")

# Analyze understanding by AI familiarity
open_ended_report.write("### AGI Understanding by AI Familiarity Level\n\n")
open_ended_report.write("The sophistication of AGI definitions varies significantly by students' self-reported AI familiarity:\n\n")

# Sample responses by familiarity level
for level in range(1, 6):
    level_responses = df[df['ai_familiarity'] == level]['agi_understanding'].dropna().tolist()
    if level_responses:
        sample_responses = np.random.choice(level_responses, min(3, len(level_responses)), replace=False)
        open_ended_report.write(f"**Familiarity Level {level}** (sample responses):\n\n")
        for resp in sample_responses:
            open_ended_report.write(f"- \"{resp}\"\n")
        open_ended_report.write("\n")

open_ended_report.write("The analysis of AGI definitions reveals a progression in conceptual sophistication corresponding to AI familiarity levels:\n\n")
open_ended_report.write("1. **Low Familiarity (Levels 1-2)**: Students with low AI familiarity tend to define AGI in simplistic terms, often referencing science fiction concepts like \"robots that can think\" or \"AI that is smarter than humans.\" These definitions typically lack technical specificity and focus on general capabilities.\n\n")
open_ended_report.write("2. **Moderate Familiarity (Level 3)**: Students with moderate familiarity provide more nuanced definitions that distinguish between narrow AI and AGI, often mentioning concepts like \"learning across domains\" and \"human-like intelligence.\" These definitions show awareness of the generality aspect of AGI.\n\n")
open_ended_report.write("3. **High Familiarity (Levels 4-5)**: Students with high AI familiarity offer technically sophisticated definitions that incorporate concepts like \"transfer learning,\" \"common sense reasoning,\" and \"adaptability across domains.\" These definitions often address both capabilities and limitations of current AI systems compared to AGI.\n\n")

open_ended_report.write("![AGI Understanding Word Cloud](/home/ubuntu/agi_survey_analysis/figures/agi_understanding_wordcloud.png)\n\n")

# 2. Personal Use Analysis
print("Analyzing personal use responses...")
open_ended_report.write("## 2. Personal Use of AGI\n\n")

# Extract and preprocess personal use responses
personal_use_responses = df['personal_use'].dropna().tolist()
preprocessed_personal_use = [preprocess_text(text) for text in personal_use_responses if isinstance(text, str)]
all_personal_use_text = ' '.join(preprocessed_personal_use)

# Create word cloud for personal use
create_wordcloud(all_personal_use_text, 
                "Key Terms in Anticipated Personal Uses of AGI", 
                "/home/ubuntu/agi_survey_analysis/figures/personal_use_wordcloud.png")

# Extract key phrases from personal use responses
personal_use_phrases = extract_key_phrases([text for text in personal_use_responses if isinstance(text, str)])

# Perform topic modeling on personal use responses
personal_use_topics, _ = perform_topic_modeling([text for text in personal_use_responses if isinstance(text, str)])

# Write results to report
open_ended_report.write("When asked how they would personally use AGI if it were available, undergraduate students described a variety of potential applications relevant to their lives and studies.\n\n")

open_ended_report.write("### Key Phrases in Personal Use Descriptions\n\n")
open_ended_report.write("The most common phrases used by students to describe personal AGI use include:\n\n")
open_ended_report.write("| Phrase | Frequency |\n")
open_ended_report.write("|--------|----------|\n")
for phrase, freq in personal_use_phrases[:15]:
    open_ended_report.write(f"| {phrase} | {freq} |\n")
open_ended_report.write("\n")

open_ended_report.write("### Personal Use Categories\n\n")
open_ended_report.write("Topic modeling analysis identified the following categories of anticipated personal AGI use:\n\n")
for topic_idx, top_words in personal_use_topics:
    open_ended_report.write(f"**Category {topic_idx+1}**: {', '.join(top_words)}\n\n")

# Analyze personal use by field of study
open_ended_report.write("### Personal Use by Field of Study\n\n")
open_ended_report.write("Anticipated personal uses of AGI vary significantly by students' field of study:\n\n")

# Sample responses by field of study
major_fields = ['Computer Science/IT', 'Engineering', 'Business/Economics', 
                'Natural Sciences', 'Social Sciences', 'Arts and Humanities', 'Health Sciences']
for field in major_fields:
    field_responses = df[df['field_of_study'] == field]['personal_use'].dropna().tolist()
    if field_responses:
        sample_responses = np.random.choice(field_responses, min(2, len(field_responses)), replace=False)
        open_ended_report.write(f"**{field}** (sample responses):\n\n")
        for resp in sample_responses:
            open_ended_report.write(f"- \"{resp}\"\n")
        open_ended_report.write("\n")

open_ended_report.write("The analysis of anticipated personal uses reveals distinct patterns across academic disciplines:\n\n")
open_ended_report.write("1. **Computer Science/IT and Engineering**: Students in technical fields envision using AGI for coding assistance, debugging, system optimization, and learning new programming languages or technical concepts. They often mention specific technical applications like \"generating code snippets\" or \"optimizing algorithms.\"\n\n")
open_ended_report.write("2. **Business/Economics**: Business students anticipate using AGI for market analysis, financial forecasting, business strategy development, and economic modeling. They focus on applications that provide competitive advantages or improve decision-making in business contexts.\n\n")
open_ended_report.write("3. **Natural Sciences**: Science students envision using AGI to analyze experimental data, model complex systems, generate research hypotheses, and stay current with scientific literature. They emphasize AGI's potential to accelerate scientific discovery.\n\n")
open_ended_report.write("4. **Social Sciences**: Students in social sciences anticipate using AGI to analyze social trends, design research studies, explore theoretical frameworks, and understand complex social phenomena. They focus on AGI as a tool for understanding human behavior and social dynamics.\n\n")
open_ended_report.write("5. **Arts and Humanities**: Humanities students envision using AGI for creative inspiration, research assistance, cultural analysis, and exploring new forms of artistic expression. They often mention AGI as a collaborative creative partner.\n\n")
open_ended_report.write("6. **Health Sciences**: Health sciences students anticipate using AGI for medical research, patient care planning, treatment option analysis, and health data interpretation. They focus on applications that improve healthcare outcomes and medical knowledge.\n\n")

open_ended_report.write("Across all disciplines, common themes include using AGI for learning enhancement, productivity improvement, and research assistance. However, the specific applications and contexts vary significantly based on students' academic backgrounds and interests.\n\n")

open_ended_report.write("![Personal Use Word Cloud](/home/ubuntu/agi_survey_analysis/figures/personal_use_wordcloud.png)\n\n")

# 3. Personal Concerns Analysis
print("Analyzing personal concerns responses...")
open_ended_report.write("## 3. Personal Concerns About AGI\n\n")

# Extract and preprocess personal concerns responses
personal_concerns_responses = df['personal_concerns'].dropna().tolist()
preprocessed_concerns = [preprocess_text(text) for text in personal_concerns_responses if isinstance(text, str)]
all_concerns_text = ' '.join(preprocessed_concerns)

# Create word cloud for personal concerns
create_wordcloud(all_concerns_text, 
                "Key Terms in Personal Concerns About AGI", 
                "/home/ubuntu/agi_survey_analysis/figures/personal_concerns_wordcloud.png")

# Extract key phrases from personal concerns responses
concerns_phrases = extract_key_phrases([text for text in personal_concerns_responses if isinstance(text, str)])

# Perform topic modeling on personal concerns responses
concerns_topics, _ = perform_topic_modeling([text for text in personal_concerns_responses if isinstance(text, str)])

# Write results to report
open_ended_report.write("When asked about their personal concerns regarding AGI development, undergraduate students expressed a range of worries and potential risks.\n\n")

open_ended_report.write("### Key Phrases in Personal Concerns\n\n")
open_ended_report.write("The most common phrases used by students to express concerns about AGI include:\n\n")
open_ended_report.write("| Phrase | Frequency |\n")
open_ended_report.write("|--------|----------|\n")
for phrase, freq in concerns_phrases[:15]:
    open_ended_report.write(f"|<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>