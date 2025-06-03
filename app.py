import streamlit as st
from model import (
    extract_name, extract_email, extract_skills, 
    extract_education, SKILLSET, extract_contact_info
)

st.set_page_config(page_title="Resume Parser", layout="wide")

st.title("📄 Resume Parser")
st.write("Upload your resume text to extract key information")

# Text input area for resume
resume_text = st.text_area("Paste your resume text here:", height=300)

if st.button("Parse Resume"):
    if resume_text:
        with st.spinner("Analyzing resume..."):
            # Extract information
            name = extract_name(resume_text)
            contact_info = extract_contact_info(resume_text)
            skills = extract_skills(resume_text)
            education = extract_education(resume_text)

            # Display results in a nice format
            st.header("Extracted Information")
            
            # Personal Information Section
            st.subheader("👤 Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Name:** {name if name else 'Not found'}")
                if contact_info['emails']:
                    st.write(f"**Email:** {', '.join(contact_info['emails'])}")
                if contact_info['phones']:
                    st.write(f"**Phone:** {', '.join(contact_info['phones'])}")
            
            with col2:
                if contact_info['linkedin']:
                    st.write(f"**LinkedIn:** {', '.join(contact_info['linkedin'])}")
                if contact_info['github']:
                    st.write(f"**GitHub:** {', '.join(contact_info['github'])}")
            
            # Education Section
            st.subheader("🎓 Education")
            if education:
                for edu in education:
                    # Format the degree and major
                    degree_line = edu['degree']
                    if edu['major']:
                        degree_line += f" in {edu['major']}"
                    
                    # Format the institution and date range
                    institution_line = ""
                    if edu['institution']:
                        institution_line = edu['institution']
                        if edu['date_range']:
                            institution_line += f" — {edu['date_range']}"
                    
                    # Display the formatted education entry
                    st.write(f"**{degree_line}**")
                    if institution_line:
                        st.write(f"*{institution_line}*")
                    st.write("---")
            else:
                st.write("No education information found")
            
            # Skills Section
            st.subheader("🛠️ Skills")
            if skills:
                # Group skills by category
                categorized_skills = {}
                for skill in skills:
                    for category, skill_list in SKILLSET.items():
                        if skill.lower() in [s.lower() for s in skill_list]:
                            if category not in categorized_skills:
                                categorized_skills[category] = []
                            categorized_skills[category].append(skill)
                            break
                    else:
                        if 'other' not in categorized_skills:
                            categorized_skills['other'] = []
                        categorized_skills['other'].append(skill)
                
                # Display skills by category in columns
                cols = st.columns(3)
                for i, (category, skill_list) in enumerate(categorized_skills.items()):
                    with cols[i % 3]:
                        st.write(f"**{category.replace('_', ' ').title()}**")
                        for skill in skill_list:
                            st.write(f"- {skill}")
            else:
                st.write("No skills found")
    else:
        st.warning("Please enter some resume text to parse.")
