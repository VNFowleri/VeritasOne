import streamlit as st
import pandas as pd
import time
import os

# Ensure the logo is in the correct directory
logo_filename = "logo.png"
logo_path = os.path.join(os.path.dirname(__file__), logo_filename)  # Get full path

st.sidebar.title("Veritas One")
page = st.sidebar.radio("Navigation",
                        ["Home", "What We Do", "How Your Data is Used", "Register", "Dashboard", "Upload Data",
                         "Earnings", "Backend"])

# Simulated User Data (Mock Backend)
user_data = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "dob": "1990-01-01",
    "data_sharing": "Research Only",
    "earnings": 15.25,
    "fhir_data": [
        {
            "Date": "01-22-2025",
            "Encounter": "Primary Care Visit",
            "Provider": "Dr. V. Singh",
            "Location": "Massachusetts General Hospital",
            "Diagnosis": ["Hypertension", "Diabetes"],
            "Medications": ["Metformin", "Lisinopril"]
        },
        {
            "Date": "02-22-2025",
            "Encounter": "Urology Outpatient",
            "Provider": "Dr. M. Thoman",
            "Location": "Massachusetts General Hospital",
            "Diagnosis": ["Nephrolithiasis"],
            "Procedures": ["Lithotripsy"]
        }
    ]
}

# Home Page
if page == "Home":
    st.title("Welcome to Veritas One")
    st.write("Manage and monetize your health data securely.")

    # Display logo only on the Home page
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.warning("⚠️ Logo file not found. Please check the filename and path.")

    st.markdown("### Get Started")
    st.button("Sign Up", on_click=lambda: st.experimental_set_query_params(page="Register"))
    st.button("Log In", on_click=lambda: st.experimental_set_query_params(page="Dashboard"))

# What We Do Page
elif page == "What We Do":
    st.title("What We Do")
    st.markdown("""
    **Veritas One represents a paradigm shift in patient data ownership** by enabling individuals to aggregate, access, and monetize their health records.  
    Currently, electronic health record (EHR) fragmentation remains a substantial barrier to coordinated care, patient autonomy, and equitable data monetization.  
    Despite health data being a multi-billion-dollar industry, patients lack direct control over their own information and receive no financial benefit from its use in research or advertising.

    ### **Our platform directly addresses these challenges by:**
    - **Providing a centralized patient-controlled health record** that integrates structured FHIR-based EHR data, faxed documents, and DICOM imaging.
    - **Offering a transparent compensation model** where patients can opt to share de-identified data for research or identifiable data for targeted health-related advertising, ensuring ethical and controlled monetization.
    - **Empowering patients** to reduce redundant tests, enhance care coordination, and facilitate second opinions, ultimately reducing healthcare inefficiencies and improving outcomes.

    **At Veritas One, you own your health data, you control its use, and you benefit from it.**
    """)

# How Your Data is Used Page
elif page == "How Your Data is Used":
    st.title("How Your Health Data is Stored & Used")
    st.markdown("""
    At Veritas One, we use a **two-database system** to keep your identifiable and de-identified data separate. This ensures your privacy while still allowing you to benefit from data sharing.

    **1. Your Identifiable Data (Stored in a Secure Personal Health Record)**
    - **What it includes:** Your name, date of birth, medical history, lab results, provider notes, imaging, medications, and other personal health records.
    - **Where it’s stored:** In a secure, HIPAA-compliant personal health record that only you can access and share.
    - **Who can see it?** Only you, and anyone you explicitly choose to share it with.

    **2. Your De-Identified Data (Used for Medical Research & Insights)**
    - **What it includes:** Medical conditions, treatments, lab values, imaging findings—but with all personal identifiers removed (no name, date of birth, or anything traceable back to you).
    - **Where it’s stored:** In a separate research database used to improve medicine, public health, and clinical care.
    - **Who can see it?** Researchers and healthcare analysts, but they will never see your name, contact information, or anything that could identify you.
    """)

# Registration Page
elif page == "Register":
    st.title("Patient Registration")
    with st.form("register_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        dob = st.date_input("Date of Birth")
        consent = st.checkbox("I agree to the Terms and Conditions")
        sharing_preference = st.radio("Data Sharing Preferences",
                                      ["None", "Research Only (5%)", "Research + Ads (15%)"],
                                      help="Select how your data is shared and how you can earn.")
        submit = st.form_submit_button("Register")
        if submit and consent:
            st.success("Registration Successful! Redirecting to Dashboard...")
            time.sleep(2)
            st.experimental_set_query_params(page="Dashboard")

# Dashboard Page
elif page == "Dashboard":
    st.title("Patient Dashboard")
    st.subheader(f"Welcome, {user_data['name']}")
    st.markdown("### Your Health Data")
    df = pd.DataFrame(user_data["fhir_data"])
    st.dataframe(df)
    st.markdown("### Your Data Control")
    st.write(f"**Current Data Sharing Setting:** {user_data['data_sharing']}")
    st.markdown("### Earnings Overview")
    st.metric("Total Earnings", f"${user_data['earnings']:.2f}")

# Upload Data Page
elif page == "Upload Data":
    st.title("Upload Medical Records")
    uploaded_file = st.file_uploader("Upload a Medical Record (PDF, JPG, PNG)", type=["pdf", "jpg", "png"])
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

# Earnings Page
elif page == "Earnings":
    st.title("Your Earnings")
    st.metric("💰 Total Earnings", f"${user_data['earnings']:.2f}")

    st.markdown("### Adjust Data Sharing Level")
    new_preference = st.radio("Change Sharing Preference", ["None", "Research Only (5%)", "Research + Ads (15%)"])
    st.success(f"✅ Updated preference: {new_preference}")

    if st.button("Go to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.experimental_rerun()

# Backend
elif page == "Backend":
    st.title("Backend Simulation")
    st.markdown("### 1. Mock FHIR API Query")
    st.json(user_data["fhir_data"])
    st.markdown("### 2. Upload & OCR a Sample Record")
    demo_file = st.file_uploader("Upload a Sample Record", type=["pdf", "jpg", "png"])
    if demo_file:
        st.success("File uploaded! Processing OCR...")
        time.sleep(2)
        st.write("Extracted Data: **Example OCR Output**")

st.sidebar.markdown("---")
st.sidebar.markdown("Built for Veritas One")
st.sidebar.markdown("BTG Health Consulting")