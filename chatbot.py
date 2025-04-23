import streamlit as st
import json
import os
import pandas as pd
from groq import Groq
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Medical Symptom Analyzer",
    page_icon="🏥",
    layout="wide"
)

# Initialize Groq client with API key from .env
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

# Function to load doctors database from CSV
@st.cache_data
def load_doctors_database():
    try:
        # Try to load from CSV file
        df = pd.read_csv("doctors_database.csv")
        # Convert DataFrame to list of dictionaries
        return df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error loading doctors database: {e}")
        # Return a default database as fallback
        return [
            {"name": "Dr. Alice Johnson", "specialization": "Cardiology", "experience": "15 years", "contact": "555-0123"},
            {"name": "Dr. Robert Smith", "specialization": "Neurology", "experience": "12 years", "contact": "555-0124"},
            {"name": "Dr. Jennifer Garcia", "specialization": "General Practice", "experience": "8 years", "contact": "555-0133"},
        ]

# Load doctors database
DOCTORS_DATABASE = load_doctors_database()


def generate_medical_response(symptoms, doctors_data):
    """Use Groq API to analyze symptoms and recommend doctors"""
    
    system_prompt = f"""
    You are a medical assistant chatbot designed to provide preliminary analysis of symptoms.
    
    Your responsibilities are:
    1. Analyze the symptoms provided by the user
    2. Identify possible conditions that match these symptoms (list 2-4 possibilities with varying levels of severity)
    3. Suggest general treatment approaches for each condition
    4. Recommend which type of specialist the user should consult
    5. Recommend specific doctors from the database based on the appropriate specialization

    Always include appropriate medical disclaimers and encourage seeking professional medical advice.
    
    Doctor database: {json.dumps(doctors_data)}
    
    IMPORTANT: Your response must be in valid JSON format with the following structure:
    {{
        "possible_conditions": [
            {{
                "condition": "Name of condition",
                "likelihood": "low/medium/high",
                "description": "Brief description",
                "general_treatment": "General treatment approaches",
                "recommended_specialist": "Type of specialist"
            }}
        ],
        "recommended_doctors": [
            {{
                "name": "Doctor name",
                "specialization": "Doctor specialization",
                "experience": "Experience",
                "contact": "Contact info"
            }}
        ],
        "general_advice": "General advice about the symptoms",
        "disclaimer": "Medical disclaimer"
    }}
    """
    user_message = f"Analyze these symptoms: {symptoms}"
    
    try:
        with st.spinner('Analyzing your symptoms... Please wait.'):
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_completion_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
    
    except Exception as e:
        return {
            "error": f"An error occurred: {str(e)}",
            "possible_conditions": [],
            "recommended_doctors": [],
            "general_advice": "Unable to analyze symptoms at this time.",
            "disclaimer": "This is not medical advice. Please consult a healthcare professional."
        }


def display_doctors_list():
    """Display the list of all available doctors"""
    st.header("Our Medical Specialists")
    
    # Add search and filter options
    st.subheader("Find a Doctor")
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input("Search by name or keyword:")
    
    with col2:
        specialties = [doc["specialization"] for doc in DOCTORS_DATABASE]
        specialties = sorted(list(set(specialties)))
        selected_specialty = st.selectbox("Filter by specialty:", ["All Specialties"] + specialties)
    
    # Filter doctors based on search and specialty
    filtered_doctors = DOCTORS_DATABASE
    if search_term:
        filtered_doctors = [doc for doc in filtered_doctors if search_term.lower() in doc["name"].lower() or 
                           (doc.get("specialization") and search_term.lower() in doc["specialization"].lower())]
    
    if selected_specialty != "All Specialties":
        filtered_doctors = [doc for doc in filtered_doctors if doc.get("specialization") == selected_specialty]
    
    # Display number of results
    st.write(f"Found {len(filtered_doctors)} doctors")
    
    if not filtered_doctors:
        st.info("No doctors match your search criteria. Please try different keywords or filters.")
        return
    
    # Create a grid layout for doctors
    cols = st.columns(3)
    
    for i, doctor in enumerate(filtered_doctors):
        col_idx = i % 3
        
        with cols[col_idx]:
            with st.container():
                st.markdown(f"### {doctor['name']}")
                st.markdown(f"**Specialization:** {doctor.get('specialization', 'N/A')}")
                st.markdown(f"**Experience:** {doctor.get('experience', 'N/A')}")
                
                # Check for additional fields
                if 'hospital' in doctor:
                    st.markdown(f"**Hospital:** {doctor['hospital']}")
                if 'availability' in doctor:
                    st.markdown(f"**Availability:** {doctor['availability']}")
                
                # Contact and rating in same row
                contact_rating_col1, contact_rating_col2 = st.columns(2)
                with contact_rating_col1:
                    st.markdown(f"**Contact:** {doctor.get('contact', 'N/A')}")
                if 'rating' in doctor:
                    with contact_rating_col2:
                        st.markdown(f"**Rating:** {'⭐' * int(float(doctor['rating']))}")
                
                # Expandable details section
                with st.expander("More Details"):
                    if 'address' in doctor:
                        st.markdown(f"**Address:** {doctor['address']}")
                    if 'languages' in doctor:
                        st.markdown(f"**Languages:** {doctor['languages']}")
                    if 'education' in doctor:
                        st.markdown(f"**Education:** {doctor['education']}")
                
                # Book appointment button
                st.button(f"Book with Dr. {doctor['name'].split()[-1]}", key=f"book_{i}")
                
                # Add separator
                st.markdown("---")


def display_medical_response(response):
    """Display the medical response in a user-friendly format"""
    # Display error if present
    if "error" in response:
        st.error(f"Error: {response['error']}")
        st.warning("Unable to analyze symptoms at this time.")
        return
    
    # Display general advice
    st.subheader("General Advice")
    st.info(response["general_advice"])
    
    # Display possible conditions
    st.subheader("Possible Conditions")
    
    for condition in response["possible_conditions"]:
        likelihood = condition["likelihood"].lower()
        if likelihood == "high":
            color = "🔴"
        elif likelihood == "medium":
            color = "🟠"
        else:
            color = "🟢"
            
        with st.expander(f"{color} {condition['condition']} (Likelihood: {condition['likelihood']})"):
            st.markdown(f"**Description:** {condition['description']}")
            st.markdown(f"**General Treatment:** {condition['general_treatment']}")
            st.markdown(f"**Recommended Specialist:** {condition['recommended_specialist']}")
    
    # Display recommended doctors
    if response["recommended_doctors"]:
        st.subheader("Recommended Doctors")
        cols = st.columns(min(3, len(response["recommended_doctors"])))
        
        for i, doctor in enumerate(response["recommended_doctors"]):
            col_index = i % len(cols)
            with cols[col_index]:
                st.markdown(f"### {doctor['name']}")
                st.markdown(f"**Specialization:** {doctor['specialization']}")
                st.markdown(f"**Experience:** {doctor['experience']}")
                st.markdown(f"**Contact:** {doctor['contact']}")
                
                # Check for additional fields
                doctor_full_data = next((d for d in DOCTORS_DATABASE if d["name"] == doctor["name"]), None)
                if doctor_full_data:
                    if 'hospital' in doctor_full_data:
                        st.markdown(f"**Hospital:** {doctor_full_data['hospital']}")
                    if 'rating' in doctor_full_data:
                        st.markdown(f"**Rating:** {'⭐' * int(float(doctor_full_data['rating']))}")
                
                st.button(f"Contact Dr. {doctor['name'].split()[-1]}", key=f"contact_{i}")
    
    # Display disclaimer
    st.markdown("---")
    st.caption(response["disclaimer"])


def main():
    # App title and description
    st.title("🏥 Medical Symptom Analyzer")
    st.markdown(
        """
        This application helps analyze your symptoms and suggests possible conditions 
        and specialist doctors you might want to consult.
        
        **Note:** This is not a replacement for professional medical advice.
        """
    )
    
    # Create sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio("Go to", ["Symptom Analysis", "Find a Doctor", "About Us"])
        
        st.markdown("---")
        st.markdown("### About")
        st.info(
            """
            This application uses AI to analyze symptoms and 
            provide preliminary medical guidance. Always consult 
            a healthcare professional for proper diagnosis and treatment.
            """
        )
    
    # Main content based on selected page
    if page == "Symptom Analysis":
        st.header("Describe Your Symptoms")
        
        # Create a form for symptoms input
        with st.form(key="symptom_form"):
            symptoms = st.text_area(
                "Please describe your symptoms in detail:",
                height=150,
                placeholder="Example: I've been experiencing severe headaches for the past 3 days, along with nausea and sensitivity to light..."
            )
            
            submit_button = st.form_submit_button(label="Analyze Symptoms")
        if submit_button and symptoms.strip():
            response = generate_medical_response(symptoms, DOCTORS_DATABASE)
            if "error" not in response:
                st.success("Analysis completed!")
            display_medical_response(response)       
        elif submit_button and not symptoms.strip():
            st.error("Please describe your symptoms before submitting.")
        with st.expander("Need help describing symptoms?"):
            st.markdown(
                """
                **Tips for describing symptoms effectively:**
                - Note when symptoms started
                - Describe the severity (mild, moderate, severe)
                - Mention if anything makes symptoms better or worse
                - Include any relevant medical history
                
                **Sample symptom descriptions:**
                1. "I've had a dry cough for about 2 weeks, with occasional chest tightness and shortness of breath when exercising."
                2. "Experiencing sharp abdominal pain on the lower right side for 24 hours, with nausea and loss of appetite."
                3. "Frequent headaches on the right side of my head, throbbing pain, worse in the morning and when bending over."
                """
            )
    elif page == "Find a Doctor":
        display_doctors_list()
    else:  # About Us page
        st.header("About Medical Symptom Analyzer")
        st.subheader("Our Mission")
        st.write(
            """
            Medical Symptom Analyzer was developed to bridge the gap between symptom awareness and professional 
            medical consultation. Our tool provides preliminary insights to help you understand potential causes 
            for your symptoms and connect you with appropriate specialists.
            """
        )
        st.subheader("How It Works")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 1. Describe Symptoms")
            st.markdown("Enter detailed description of your symptoms, their duration, severity, and any relevant medical history.")
        
        with col2:
            st.markdown("### 2. AI Analysis")
            st.markdown("Our advanced AI system processes your symptoms against a comprehensive medical knowledge base.")
        
        with col3:
            st.markdown("### 3. Get Recommendations")
            st.markdown("Receive potential conditions and recommended specialists to consult for proper diagnosis.")
        st.subheader("Important Disclaimer")
        st.warning(
            """
            This tool is designed for informational purposes only and should not replace professional medical advice, 
            diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider 
            with any questions you may have regarding a medical condition.
            """
        )
if __name__ == "__main__":
    main()