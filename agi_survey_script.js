/**
 * AGI Research Survey Script
 * 
 * This script creates a Google Form for researching undergraduate perspectives on AGI.
 * To use this script:
 * 1. Go to https://script.google.com/
 * 2. Create a new project
 * 3. Copy and paste this entire script
 * 4. Save the project (Ctrl+S or File > Save)
 * 5. Run the createAGISurvey function (Run > Run function > createAGISurvey)
 * 6. Authorize the script when prompted
 * 7. Check your Google Drive for the newly created form
 */

function createAGISurvey() {
  // Create a new form
  var form = FormApp.create('Undergraduate Perspectives on Artificial General Intelligence (AGI)');
  
  // Set form description and other properties
  form.setDescription('This research survey aims to understand undergraduate students\' attitudes, expectations, and concerns regarding Artificial General Intelligence (AGI). Your responses will contribute to academic research on how future generations perceive emerging AI technologies. All responses are confidential and will be used for research purposes only. Estimated completion time: 15-20 minutes.');
  form.setConfirmationMessage('Thank you for participating in this research survey on undergraduate perspectives on Artificial General Intelligence. Your responses will contribute to our understanding of how future generations perceive emerging AI technologies.');
  form.setAllowResponseEdits(true);
  form.setCollectEmail(true);
  
  // Add consent information
  var consentItem = form.addSectionHeaderItem();
  consentItem.setTitle('Consent Information')
    .setHelpText('By completing this survey, you consent to participate in this research study. Your participation is voluntary, and you may exit the survey at any time. Your responses will be kept confidential and analyzed in aggregate form.');
  
  // DEMOGRAPHICS SECTION
  var demographicsHeader = form.addSectionHeaderItem();
  demographicsHeader.setTitle('Demographics')
    .setHelpText('Please provide some basic information about yourself.');
  
  // Age
  var ageItem = form.addMultipleChoiceItem();
  ageItem.setTitle('What is your age?')
    .setChoiceValues(['18-19', '20-21', '22-23', '24-25', '26+'])
    .setRequired(true);
  
  // Gender
  var genderItem = form.addMultipleChoiceItem();
  genderItem.setTitle('What is your gender?')
    .setChoiceValues(['Male', 'Female', 'Non-binary/third gender', 'Prefer to self-describe', 'Prefer not to say'])
    .setRequired(true);
  
  // Academic Year
  var yearItem = form.addMultipleChoiceItem();
  yearItem.setTitle('What is your current academic year?')
    .setChoiceValues(['Freshman', 'Sophomore', 'Junior', 'Senior', 'Other'])
    .setRequired(true);
  
  // Field of Study
  var fieldItem = form.addMultipleChoiceItem();
  fieldItem.setTitle('What is your primary field of study?')
    .setChoiceValues([
      'Arts and Humanities', 
      'Social Sciences', 
      'Business/Economics', 
      'Natural Sciences', 
      'Computer Science/IT', 
      'Engineering', 
      'Health Sciences', 
      'Education', 
      'Other'
    ])
    .setRequired(true);
  
  // AI Familiarity
  var familiarityItem = form.addScaleItem();
  familiarityItem.setTitle('How would you rate your familiarity with artificial intelligence concepts?')
    .setBounds(1, 5)
    .setLabels('Not at all familiar', 'Very familiar')
    .setRequired(true);
  
  // Technical Background
  var technicalItem = form.addScaleItem();
  technicalItem.setTitle('How would you rate your technical/programming background?')
    .setBounds(1, 5)
    .setLabels('No technical background', 'Strong technical background')
    .setRequired(true);
  
  // Information Sources
  var sourcesItem = form.addCheckboxItem();
  sourcesItem.setTitle('Where do you typically get information about AI developments? (Select all that apply)')
    .setChoiceValues([
      'Academic courses', 
      'Scientific publications', 
      'News media', 
      'Social media', 
      'Movies/TV shows', 
      'Friends/family', 
      'I don\'t follow AI developments'
    ])
    .setRequired(true);
  
  // ATTITUDES TOWARD AGI SECTION
  var attitudesPageBreak = form.addPageBreakItem();
  attitudesPageBreak.setTitle('Attitudes Toward AGI')
    .setHelpText('This section explores your general understanding and feelings about Artificial General Intelligence (AGI).');
  
  // AGI Understanding
  var understandingItem = form.addParagraphTextItem();
  understandingItem.setTitle('In your own words, what do you understand by the term "Artificial General Intelligence (AGI)"?')
    .setRequired(true);
  
  // AGI Timeline
  var timelineItem = form.addMultipleChoiceItem();
  timelineItem.setTitle('When do you think human-level artificial general intelligence might be developed?')
    .setChoiceValues([
      'It already exists', 
      'Within the next 10 years', 
      'Within 10-25 years', 
      'Within 25-50 years', 
      'Within 50-100 years', 
      'More than 100 years from now', 
      'Never'
    ])
    .setRequired(true);
  
  // General Sentiment
  var sentimentItem = form.addScaleItem();
  sentimentItem.setTitle('Overall, how do you feel about the development of AGI?')
    .setBounds(1, 5)
    .setLabels('Very negative', 'Very positive')
    .setRequired(true);
  
  // Interest Level
  var interestItem = form.addScaleItem();
  interestItem.setTitle('How interested are you in following developments in AGI?')
    .setBounds(1, 5)
    .setLabels('Not at all interested', 'Very interested')
    .setRequired(true);
  
  // ANTICIPATED USES OF AGI SECTION
  var usesPageBreak = form.addPageBreakItem();
  usesPageBreak.setTitle('Anticipated Uses of AGI')
    .setHelpText('This section explores how you think AGI might be used in various contexts.');
  
  // Potential Applications Grid
  var applicationsItem = form.addGridItem();
  applicationsItem.setTitle('How likely do you think AGI will be used in the following areas?')
    .setRows([
      'Education', 
      'Healthcare', 
      'Scientific research', 
      'Entertainment', 
      'Personal assistance', 
      'Business/finance', 
      'Military/defense'
    ])
    .setColumns([
      'Very unlikely', 
      'Unlikely', 
      'Neutral', 
      'Likely', 
      'Very likely'
    ])
    .setRequired(true);
  
  // Personal Use
  var personalUseItem = form.addParagraphTextItem();
  personalUseItem.setTitle('How would you personally use AGI if it were available to you?');
  
  // Career Impact
  var careerItem = form.addScaleItem();
  careerItem.setTitle('To what extent do you think AGI will impact your future career?')
    .setBounds(1, 5)
    .setLabels('No impact at all', 'Transformative impact')
    .setRequired(true);
  
  // ANTICIPATED RISKS OF AGI SECTION
  var risksPageBreak = form.addPageBreakItem();
  risksPageBreak.setTitle('Anticipated Risks of AGI')
    .setHelpText('This section explores potential risks and concerns you may have about AGI development.');
  
  // Risk Level Assessment
  var riskLevelItem = form.addScaleItem();
  riskLevelItem.setTitle('How risky do you think the development of AGI is for humanity?')
    .setBounds(1, 5)
    .setLabels('Not at all risky', 'Extremely risky')
    .setRequired(true);
  
  // Specific Risks Grid
  var specificRisksItem = form.addGridItem();
  specificRisksItem.setTitle('How concerned are you about the following potential risks of AGI?')
    .setRows([
      'Loss of human jobs', 
      'Privacy violations', 
      'Autonomous weapons', 
      'Loss of human control', 
      'Social manipulation', 
      'Economic inequality', 
      'Existential risk to humanity'
    ])
    .setColumns([
      'Not concerned', 
      'Slightly concerned', 
      'Moderately concerned', 
      'Very concerned', 
      'Extremely concerned'
    ])
    .setRequired(true);
  
  // Personal Concerns
  var concernsItem = form.addParagraphTextItem();
  concernsItem.setTitle('What concerns you most about the development of AGI?');
  
  // POSSIBLE SOCIETAL BENEFITS SECTION
  var benefitsPageBreak = form.addPageBreakItem();
  benefitsPageBreak.setTitle('Possible Societal Benefits')
    .setHelpText('This section explores potential benefits that AGI might bring to society.');
  
  // Benefit Assessment
  var benefitLevelItem = form.addScaleItem();
  benefitLevelItem.setTitle('Overall, how beneficial do you think AGI will be for society?')
    .setBounds(1, 5)
    .setLabels('Not at all beneficial', 'Extremely beneficial')
    .setRequired(true);
  
  // Specific Benefits Grid
  var specificBenefitsItem = form.addGridItem();
  specificBenefitsItem.setTitle('How significant do you think the following potential benefits of AGI could be?')
    .setRows([
      'Scientific breakthroughs', 
      'Medical advancements', 
      'Educational improvements', 
      'Economic growth', 
      'Environmental solutions', 
      'Reduction in dangerous human labor', 
      'Improved decision-making'
    ])
    .setColumns([
      'Not significant', 
      'Slightly significant', 
      'Moderately significant', 
      'Very significant', 
      'Extremely significant'
    ])
    .setRequired(true);
  
  // Most Important Benefit
  var importantBenefitItem = form.addParagraphTextItem();
  importantBenefitItem.setTitle('What do you think could be the most important benefit of AGI for society?');
  
  // POSSIBLE SOCIETAL RISKS SECTION
  var societalRisksPageBreak = form.addPageBreakItem();
  societalRisksPageBreak.setTitle('Societal Implications and Governance')
    .setHelpText('This section explores broader societal implications and governance of AGI.');
  
  // Governance Importance
  var governanceItem = form.addScaleItem();
  governanceItem.setTitle('How important do you think it is to have regulations and governance for AGI development?')
    .setBounds(1, 5)
    .setLabels('Not at all important', 'Extremely important')
    .setRequired(true);
  
  // Responsibility
  var responsibilityItem = form.addMultipleChoiceItem();
  responsibilityItem.setTitle('Who do you think should have the primary responsibility for ensuring AGI is developed safely?')
    .setChoiceValues([
      'Government/regulators', 
      'Tech companies', 
      'Academic researchers', 
      'International organizations', 
      'Independent oversight bodies', 
      'The public', 
      'Other'
    ])
    .setRequired(true);
  
  // Societal Preparation
  var preparationItem = form.addScaleItem();
  preparationItem.setTitle('How prepared do you think society is for the potential impacts of AGI?')
    .setBounds(1, 5)
    .setLabels('Not at all prepared', 'Very well prepared')
    .setRequired(true);
  
  // Biggest Societal Challenge
  var challengeItem = form.addParagraphTextItem();
  challengeItem.setTitle('What do you think will be the biggest challenge for society in adapting to AGI?');
  
  // CONCLUDING QUESTIONS
  var conclusionPageBreak = form.addPageBreakItem();
  conclusionPageBreak.setTitle('Concluding Questions')
    .setHelpText('Final questions about education and your interest in AGI.');
  
  // Education Need
  var educationItem = form.addScaleItem();
  educationItem.setTitle('How important do you think it is for undergraduate education to include more content about AGI and its implications?')
    .setBounds(1, 5)
    .setLabels('Not at all important', 'Extremely important')
    .setRequired(true);
  
  // Future Involvement
  var involvementItem = form.addMultipleChoiceItem();
  involvementItem.setTitle('Would you be interested in being involved in AGI development or governance in the future?')
    .setChoiceValues([
      'Definitely yes', 
      'Probably yes', 
      'Might or might not', 
      'Probably not', 
      'Definitely not'
    ])
    .setRequired(true);
  
  // Final Thoughts
  var finalThoughtsItem = form.addParagraphTextItem();
  finalThoughtsItem.setTitle('Do you have any other thoughts or perspectives on AGI that weren\'t covered in this survey?');
  
  // Results Option
  var resultsItem = form.addMultipleChoiceItem();
  resultsItem.setTitle('Would you like to receive a summary of the research findings when available?')
    .setChoiceValues(['Yes', 'No']);
  
  // Log the published URL
  Logger.log('Published URL: ' + form.getPublishedUrl());
  Logger.log('Editor URL: ' + form.getEditUrl());
  
  // Return the form object for further use if needed
  return form;
}
