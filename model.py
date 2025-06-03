import re
import spacy
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import torch
from datetime import datetime

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Load HuggingFace model for NER
model_id = "dslim/bert-base-NER"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForTokenClassification.from_pretrained(model_id)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# Comprehensive skillset
SKILLSET = {
    'programming_languages': [
        'python', 'javascript', 'java', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust',
        'typescript', 'r', 'matlab', 'scala', 'perl', 'shell', 'bash'
    ],
    'web_frameworks': [
        'flask', 'django', 'fastapi', 'express', 'react', 'angular', 'vue', 'spring', 'laravel',
        'asp.net', 'rails', 'next.js', 'nuxt.js', 'svelte'
    ],
    'databases': [
        'postgresql', 'mongodb', 'mysql', 'sqlite', 'oracle', 'sql server', 'redis', 'cassandra',
        'elasticsearch', 'neo4j', 'dynamodb', 'firebase'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'gcp', 'google cloud', 'digital ocean', 'heroku', 'ibm cloud',
        'alibaba cloud', 'oracle cloud'
    ],
    'devops_tools': [
        'docker', 'kubernetes', 'jenkins', 'gitlab', 'github actions', 'terraform', 'ansible',
        'prometheus', 'grafana', 'nagios', 'splunk', 'elk stack'
    ],
    'version_control': [
        'git', 'svn', 'mercurial', 'bitbucket', 'github', 'gitlab'
    ],
    'api_technologies': [
        'rest', 'graphql', 'soap', 'grpc', 'microservices', 'api gateway', 'swagger',
        'openapi', 'postman'
    ],
    'ai_ml': [
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
        'pytorch', 'scikit-learn', 'keras', 'opencv', 'nltk', 'spacy', 'bert', 'gpt',
        'transformers', 'reinforcement learning', 'data science'
    ],
    'testing': [
        'unit testing', 'integration testing', 'e2e testing', 'jest', 'pytest',
        'selenium', 'cypress', 'junit', 'mockito'
    ],
    'other_skills': [
        'agile', 'scrum', 'ci/cd', 'tdd', 'bdd', 'microservices', 'serverless',
        'restful apis', 'graphql', 'websockets', 'oauth', 'jwt', 'oauth2'
    ]
}

# Function to extract email using regex
def extract_email(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)

# Function to extract skills (define your skillset for lookup)
def extract_skills(text, skillset=None):
    if not skillset:
        # Flatten the skillset dictionary into a single list
        skillset = [skill for category in SKILLSET.values() for skill in category]
    
    text = text.lower()
    skills_found = []
    
    # Check for exact matches
    for skill in skillset:
        if skill.lower() in text:
            skills_found.append(skill)
    
    # Check for variations and common abbreviations
    variations = {
        'ml': 'machine learning',
        'ai': 'artificial intelligence',
        'js': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'aws': 'amazon web services',
        'gcp': 'google cloud platform',
        'ci/cd': 'continuous integration/continuous deployment',
        'e2e': 'end to end',
        'api': 'application programming interface',
        'rest': 'representational state transfer',
        'sql': 'structured query language',
        'nosql': 'not only sql'
    }
    
    for abbr, full in variations.items():
        if abbr.lower() in text and full not in skills_found:
            skills_found.append(full)
    
    return list(set(skills_found))  # Remove duplicates

# Function to extract education using pattern
def extract_education(text):
    # Use BERT for education extraction
    ner_results = ner_pipeline(text)
    education_entities = []
    
    # Extract organizations (universities/colleges)
    orgs = []
    for entity in ner_results:
        if entity['entity_group'] == 'ORG':
            orgs.append(entity['word'])

    # Extract dates and date ranges
    date_pattern = r'\b(19|20)\d{2}\b'  # Years between 1900-2099
    date_range_pattern = r'\b(19|20)\d{2}\s*[-–]\s*(?:present|current|(?:19|20)\d{2})\b'
    dates = re.findall(date_pattern, text)
    date_ranges = re.findall(date_range_pattern, text, re.IGNORECASE)
    
    # Education keywords
    education_keywords = [
        'bachelor', 'master', 'phd', 'b.sc', 'm.sc', 'b.tech', 'm.tech',
        'bachelor of science', 'master of science', 'bachelor of arts',
        'master of arts', 'bachelor of engineering', 'master of engineering',
        'bachelor of technology', 'master of technology', 'bachelor of computer science',
        'master of computer science', 'bachelor of information technology',
        'master of information technology', 'bachelor of business administration',
        'master of business administration', 'bachelor of commerce',
        'master of commerce', 'bachelor of arts', 'master of arts'
    ]
    
    # Process text line by line to maintain context
    lines = text.split('\n')
    education_entries = []
    
    for line in lines:
        line = line.strip()
        if any(keyword in line.lower() for keyword in education_keywords):
            # Find date ranges in this line
            line_date_ranges = re.findall(date_range_pattern, line, re.IGNORECASE)
            
            # Find single dates in this line
            line_dates = re.findall(date_pattern, line)
            
            # Find organizations in this line
            line_orgs = [org for org in orgs if org.lower() in line.lower()]
            
            # Extract degree and major if present
            degree_parts = []
            if " in " in line.lower():
                degree, major = line.split(" in ", 1)
                degree_parts = [degree.strip(), major.strip()]
            else:
                degree_parts = [line.strip()]
            
            # Format the entry
            entry = {
                'degree': degree_parts[0],
                'major': degree_parts[1] if len(degree_parts) > 1 else None,
                'institution': line_orgs[0] if line_orgs else None,
                'date_range': None
            }
            
            # Add date range if found
            if line_date_ranges:
                for date_range in line_date_ranges:
                    if 'present' in date_range.lower() or 'current' in date_range.lower():
                        entry['date_range'] = f"{date_range.split('-')[0].strip()} - Present"
                    else:
                        entry['date_range'] = date_range
            # Add single date if no range found
            elif line_dates:
                entry['date_range'] = line_dates[0]
            
            education_entries.append(entry)
    
    # If no education entries found with dates, try to match organizations with dates
    if not education_entries and orgs and (dates or date_ranges):
        for org in orgs:
            # Find the closest date or date range to this organization
            org_index = text.find(org)
            closest_date = None
            min_distance = float('inf')
            
            # Check date ranges first
            for date_range in date_ranges:
                date_index = text.find(date_range)
                if date_index != -1:
                    distance = abs(org_index - date_index)
                    if distance < min_distance:
                        min_distance = distance
                        closest_date = date_range
            
            # If no date range found, check single dates
            if not closest_date:
                for date in dates:
                    date_index = text.find(date)
                    if date_index != -1:
                        distance = abs(org_index - date_index)
                        if distance < min_distance:
                            min_distance = distance
                            closest_date = date
            
            if closest_date:
                entry = {
                    'degree': None,
                    'major': None,
                    'institution': org,
                    'date_range': None
                }
                
                if 'present' in closest_date.lower() or 'current' in closest_date.lower():
                    entry['date_range'] = f"{closest_date.split('-')[0].strip()} - Present"
                else:
                    entry['date_range'] = closest_date
                
                education_entries.append(entry)
    
    return education_entries

# Function to extract name using spaCy NER
def extract_name(text):
    # Use BERT for name extraction
    ner_results = ner_pipeline(text)
    name_entities = []
    
    for entity in ner_results:
        if entity['entity_group'] == 'PER': # Using entity_group instead of entity
            name_entities.append(entity['word'])

    # If BERT found a name, return the first one
    if name_entities:
        return name_entities[0]
    
    # Fallback to spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    
    return None

def extract_contact_info(text):
    # Extract phone numbers
    phone_pattern = r'\+?[\d\s\-\(\)]{10,}'
    phones = re.findall(phone_pattern, text)
    
    # Extract emails
    emails = extract_email(text)
    
    # Extract LinkedIn profile
    linkedin_pattern = r'linkedin\.com/in/[\w\-]+'
    linkedin = re.findall(linkedin_pattern, text)
    
    # Extract GitHub profile
    github_pattern = r'github\.com/[\w\-]+'
    github = re.findall(github_pattern, text)
    
    return {
        'phones': phones,
        'emails': emails,
        'linkedin': linkedin,
        'github': github
    }
