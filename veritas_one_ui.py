import streamlit as st
import pandas as pd
import time
import os


# Ensure the logo is in the correct directory
logo_filename = "logo.png"
logo_path = os.path.join(os.path.dirname(__file__), logo_filename)  # Get full path

st.title("Welcome to VeritasOne")

# Check if the logo exists before displaying
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True)
else:
    st.warning("⚠️ Logo file not found. Please check the filename and path.")

# Simulated User Data (Mock Backend)
user_data = {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "dob": "1990-01-01",
    "data_sharing": "Research Only",
    "earnings": 15.25,
    "fhir_data": [
        {"Date": "2025-02-01", "Diagnosis": "Hypertension", "Medication": "Lisinopril"},
        {"Date": "2025-01-15", "Diagnosis": "Diabetes", "Medication": "Metformin"}
    ]
}

# Page Navigation
st.sidebar.title("VeritasOne")
page = st.sidebar.radio("Navigation",
                        ["Home", "About", "Data Privacy", "Register", "Dashboard", "Upload Data", "Earnings",
                         "Investor Demo"])

# Home Page
if page == "Home":
    st.title("Welcome to VeritasOne")
    st.write("Manage and monetize your health data securely.")

    # Display logo only if it exists
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)  # ✅ Fixed parameter
    else:
        st.warning("⚠️ Logo file not found. Please check the filename or path.")

    st.markdown("### Get Started")
    if st.button("Sign Up"):
        st.session_state["page"] = "Register"
        st.experimental_rerun()

    if st.button("Log In"):
        st.session_state["page"] = "Dashboard"
        st.experimental_rerun()

# About Page
elif page == "About":
    st.title("About VeritasOne")
    st.markdown("""
    **VeritasOne represents a paradigm shift in patient data ownership** by enabling individuals to aggregate, access, and monetize their health records.  
    Currently, electronic health record (EHR) fragmentation remains a substantial barrier to coordinated care, patient autonomy, and equitable data monetization.  
    Despite health data being a multi-billion-dollar industry, patients lack direct control over their own information and receive no financial benefit from its use in research or advertising.

    ### **Our platform directly addresses these challenges by:**
    - **Providing a centralized patient-controlled health record** that integrates structured FHIR-based EHR data, faxed documents, and DICOM imaging.
    - **Offering a transparent compensation model** where patients can opt to share de-identified data for research or identifiable data for targeted health-related advertising, ensuring ethical and controlled monetization.
    - **Empowering patients** to reduce redundant tests, enhance care coordination, and facilitate second opinions, ultimately reducing healthcare inefficiencies and improving outcomes.
    """)

# Data Privacy Page
elif page == "Data Privacy":
    st.title("How Your Health Data is Stored & Used")

    st.markdown("""
    **At Veritas One, we use a two-database system to keep your identifiable and de-identified data separate.**  
    This ensures your privacy while still allowing you to benefit from data sharing.
    """)

    st.subheader("1. Your Identifiable Data (Secure Personal Health Record)")
    st.markdown("""
    - **What it includes:** Your name, date of birth, medical history, lab results, provider notes, imaging, medications, and other personal health records.
    - **Where it’s stored:** In a secure, HIPAA-compliant personal health record that only you can access and share.
    - **How it’s used:**
        - For your own medical care – Share your records with doctors, specialists, or family members.
        - For optional personalized services – If you opt in, this data can be used to send you relevant health opportunities, such as:
            - A clinical trial that fits your condition  
            - A better medication option for your diagnosis  
            - A discount or special offer for a treatment you already use  
    - **Who can see it?** Only you, and anyone you explicitly choose to share it with.
    """)

    st.subheader("2. Your De-Identified Data (Medical Research & Insights)")
    st.markdown("""
    - **What it includes:** Medical conditions, treatments, lab values, imaging findings—but with all personal identifiers removed (no name, date of birth, or anything traceable back to you).
    - **Where it’s stored:** In a separate research database used to improve medicine, public health, and clinical care.
    - **How it’s used:**
        - **For medical research** – To help researchers find trends in diseases, improve treatments, and develop new drugs.
        - **For health system improvements** – To analyze patient outcomes and improve the quality of care.
        - **For public health studies** – To track trends in chronic diseases, rare conditions, and medication effectiveness.
    - **Who can see it?** Researchers and healthcare analysts, but they will never see your name, contact information, or anything that could identify you.
    """)

    st.subheader("Clear Examples of the Difference")

    # Comparison Table
    data = {
        "Use Case": [
            "Your doctor wants to review your past medical history before an appointment.",
            "A pharmaceutical company wants to study how a new diabetes drug is affecting blood sugar levels across thousands of patients.",
            "You want to get notified about a clinical trial that matches your medical history.",
            "A hospital wants to analyze anonymous patient data to improve post-surgery recovery times.",
            "You need to share your complete medical records with a new specialist.",
            "A health tech company wants to use large-scale anonymous patient data to improve early cancer detection."
        ],
        "Identifiable Data (Personal Record)": ["✅ Yes", "❌ No", "✅ Yes (if opted in)", "❌ No", "✅ Yes", "❌ No"],
        "De-Identified Data (Research Database)": ["❌ No", "✅ Yes", "❌ No", "✅ Yes", "❌ No", "✅ Yes"]
    }
    df = pd.DataFrame(data)
    st.table(df)

    st.subheader("Your Control, Your Choice")
    st.markdown("""
    - **If you do nothing,** your data stays completely private and is only available to you.
    - **If you opt in to research sharing,** your de-identified data may be used for research, and you’ll receive compensation.
    - **If you opt in to advertising,** you may receive personalized health offers based on your medical history, and you’ll receive the highest level of compensation.

    **Your data is never sold—you control it, you decide how it’s used, and you get paid if you choose to share it.**
    """)

# Sidebar Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Brandon T. Gaston, MD for VeritasOne**")