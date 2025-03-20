# Data Simulation Approach for AGI Survey

## Overview
This document outlines the approach for simulating 1,000 undergraduate student responses to the AGI survey. The simulation will create realistic and diverse responses that represent the student body at a typical public R1 university in the United States.

## Demographic Distribution

### Age Distribution
- 18-19: 30% (primarily freshmen)
- 20-21: 35% (primarily sophomores and juniors)
- 22-23: 25% (primarily juniors and seniors)
- 24-25: 7% (primarily seniors and non-traditional students)
- 26+: 3% (non-traditional students)

### Gender Distribution
- Male: 48%
- Female: 48%
- Non-binary/third gender: 3%
- Prefer to self-describe: 0.5%
- Prefer not to say: 0.5%

### Academic Year Distribution
- Freshman: 27%
- Sophomore: 25%
- Junior: 24%
- Senior: 22%
- Other: 2%

### Field of Study Distribution
- Arts and Humanities: 15%
- Social Sciences: 20%
- Business/Economics: 15%
- Natural Sciences: 15%
- Computer Science/IT: 10%
- Engineering: 12%
- Health Sciences: 8%
- Education: 4%
- Other: 1%

### AI Familiarity Distribution (1-5 scale)
- 1 (Not at all familiar): 15%
- 2: 25%
- 3: 35%
- 4: 20%
- 5 (Very familiar): 5%

### Technical Background Distribution (1-5 scale)
- 1 (No technical background): 20%
- 2: 25%
- 3: 30%
- 4: 15%
- 5 (Strong technical background): 10%

### Information Sources Distribution (multiple selection)
- Academic courses: 60%
- Scientific publications: 25%
- News media: 70%
- Social media: 85%
- Movies/TV shows: 50%
- Friends/family: 45%
- I don't follow AI developments: 10%

## Correlation Rules

To ensure realistic response patterns, we'll implement the following correlation rules:

1. **Field of Study & Technical Background**:
   - Computer Science/IT and Engineering students will have higher technical background scores (3-5)
   - Arts and Humanities students will have lower technical background scores (1-3)

2. **Field of Study & AI Familiarity**:
   - Computer Science/IT, Engineering, and Natural Sciences students will have higher AI familiarity
   - Other fields will have more varied AI familiarity

3. **Technical Background & AI Familiarity**:
   - Strong positive correlation between technical background and AI familiarity

4. **Age & Academic Year**:
   - 18-19 → predominantly Freshmen
   - 20-21 → predominantly Sophomores and Juniors
   - 22-23 → predominantly Juniors and Seniors
   - 24+ → predominantly Seniors and Other

5. **Information Sources & AI Familiarity**:
   - Higher AI familiarity correlates with more diverse information sources
   - Lower AI familiarity correlates with fewer information sources and higher likelihood of "I don't follow AI developments"

## Response Pattern Rules

For the attitude and opinion questions, we'll implement these patterns:

1. **AGI Understanding (open-ended)**:
   - Responses will vary based on AI familiarity level
   - Higher familiarity → more technical and nuanced definitions
   - Lower familiarity → more general or pop-culture influenced definitions

2. **AGI Timeline**:
   - Technical backgrounds tend toward longer timelines (10-25 years or 25-50 years)
   - Non-technical backgrounds show more variation, including shorter and longer timelines
   - Computer Science students more likely to select longer timelines

3. **Sentiment Toward AGI**:
   - Slight positive skew overall (mean around 3.3 on 5-point scale)
   - Technical fields slightly more positive
   - Humanities slightly more cautious

4. **Risk Assessment**:
   - Overall moderate concern (mean around 3.2 on 5-point scale)
   - Computer Science students show bimodal distribution (some very concerned, some less concerned)
   - Positive correlation between AI familiarity and nuanced risk assessment

5. **Benefit Assessment**:
   - Overall positive (mean around 3.7 on 5-point scale)
   - Technical fields more optimistic about benefits
   - Health Sciences and Education fields focused on specific application benefits

6. **Open-ended Responses**:
   - Will be generated based on the respondent's demographic profile
   - Length and complexity will correlate with AI familiarity
   - Content will reflect field of study perspectives

## Implementation Approach

1. **Generate Demographic Profiles**:
   - Create 1,000 unique demographic profiles following the distributions above
   - Apply correlation rules to ensure realistic combinations

2. **Generate Responses**:
   - For each profile, generate responses to all survey questions
   - Apply response pattern rules to ensure consistency
   - Include realistic variation and noise in the data

3. **Quality Control**:
   - Check for unrealistic combinations and correct them
   - Ensure overall distributions match expected patterns
   - Verify that open-ended responses are appropriate for the demographic profile

4. **Data Format**:
   - Prepare data in a format suitable for submission to the Google Form
   - Include all required fields and proper formatting

This simulation approach will produce a dataset that realistically represents the diversity of undergraduate perspectives on AGI at a public R1 university, with appropriate correlations between demographics and opinions.
