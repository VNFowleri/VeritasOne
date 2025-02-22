import streamlit as st
import pandas as pd
import time
import os

# Ensure the logo is in the correct directory
logo_filename = "logo.png"
logo_path = os.path.join(os.path.dirname(__file__), logo_filename)  # Get full path

st.sidebar.title("Veritas One")
page = st.sidebar.radio("Navigation",
                        ["Home", "How Your Data is Used", "Register", "Dashboard", "Upload Data", "Earnings", "Backend"])

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
# How Your Data is Used Page
if page == "How Your Data is Used":
    st.title("How Your Health Data is Stored & Used")
    st.markdown("""
    At Veritas One, we use a **two-database system** to keep your identifiable and de-identified data separate. This ensures your privacy while still allowing you to benefit from data sharing.

    **1. Your Identifiable Data (Stored in a Secure Personal Health Record)**
    - **What it includes:** Your name, date of birth, medical history, lab results, provider notes, imaging, medications, and other personal health records.
    - **Where it’s stored:** In a secure, HIPAA-compliant personal health record that only you can access and share.
    - **How it’s used:**
      - For your own medical care – You can share your records with doctors, specialists, or family members.
      - For optional personalized services – If you opt in, this data can be used to send you relevant health opportunities, such as:
        - A clinical trial that fits your condition
        - A better medication option for your diagnosis
        - A discount or special offer for a treatment you already use
    - **Who can see it?** Only you, and anyone you explicitly choose to share it with.

    **2. Your De-Identified Data (Used for Medical Research & Insights)**
    - **What it includes:** Medical conditions, treatments, lab values, imaging findings—but with all personal identifiers removed (no name, date of birth, or anything traceable back to you).
    - **Where it’s stored:** In a separate research database used to improve medicine, public health, and clinical care.
    - **How it’s used:**
      - For medical research – To help researchers find trends in diseases, improve treatments, and develop new drugs.
      - For health system improvements – To analyze patient outcomes and improve the quality of care.
      - For public health studies – To track trends in chronic diseases, rare conditions, and medication effectiveness.
    - **Who can see it?** Researchers and healthcare analysts, but they will never see your name, contact information, or anything that could identify you.

    **Your Control, Your Choice**

    At Veritas One, you have full control over how your data is used. We offer three tiers of data sharing, allowing you to decide what works best for you:

    **1. No Data Sharing (Strict Privacy Mode)**
    - Your data remains completely private and is stored solely for your personal use and for use with your providers and health facilities you elect to share with.
    - No compensation is provided.
    - A small service fee may apply for longitudinal data storage unless financial hardship is demonstrated.

    **2. De-Identified Research Only**
    - Your health data is used for research, but all personal identifiers are removed.
    - Researchers can analyze trends in diseases and treatments without knowing who you are.
    - You receive **5%** of profits generated from research licensing.

    **3. Full Data Sharing (Research + Advertising)**
    - Your de-identified data is used for research **AND** you opt to share select identifiable health data (such as medications or conditions) for targeted health-related advertising.
    - You receive **15%** of profits generated from your data.
    - This may include personalized health offers, clinical trial opportunities, or relevant treatment options.

    **Data Sharing Examples**

    | Use Case | No Data Sharing | De-Identified Research Only | Full Data Sharing |
    |----------------|-----------------|----------------------------|-------------------|
    | Your doctor wants to review your past medical history before an appointment. | ✅ Yes | ✅ Yes | ✅ Yes |
    | A pharmaceutical company wants to study how a new diabetes drug is affecting blood sugar levels across thousands of patients. | ❌ No | ✅ Yes | ✅ Yes |
    | You want to get notified about a clinical trial that matches your medical history. | ❌ No | ❌ No | ✅ Yes |
    | A hospital wants to analyze anonymous patient data to improve post-surgery recovery times. | ❌ No | ✅ Yes | ✅ Yes |
    | You need to share your complete medical records with a new specialist. | ✅ Yes | ✅ Yes | ✅ Yes |
    | A health tech company wants to use large-scale anonymous patient data to improve early cancer detection. | ❌ No | ✅ Yes | ✅ Yes |
    | A pharmaceutical company wants to send you targeted offers for medications based on your current prescriptions. | ❌ No | ❌ No | ✅ Yes |

    **Still have questions? We’re here to help.**
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
    if st.button("Change Sharing Preferences"):
        st.experimental_set_query_params(page="Earnings")
    st.markdown("### Uploaded Documents")
    st.write("No documents uploaded yet.")
    st.markdown("### Earnings Overview")
    st.metric("Total Earnings", f"${user_data['earnings']:.2f}")

# Upload Data Page
elif page == "Upload Data":
    st.title("Upload Medical Records")
    uploaded_file = st.file_uploader("Upload a Medical Record (PDF, JPG, PNG)", type=["pdf", "jpg", "png"])
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.write("Processing OCR...")
        time.sleep(3)
        st.write("Extracted Text: **Example Medical Report Data**")
    st.button("Go to Dashboard", on_click=lambda: st.experimental_set_query_params(page="Dashboard"))

# Earnings Page
elif page == "Earnings":
    st.title("Your Earnings")
    st.metric("Total Earnings", f"${user_data['earnings']:.2f}")
    st.markdown("### Adjust Data Sharing Level")
    new_preference = st.radio("Change Sharing Preference", ["None", "Research Only (5%)", "Research + Ads (15%)"])
    st.success(f"Updated preference: {new_preference}")
    st.button("Go to Dashboard", on_click=lambda: st.experimental_set_query_params(page="Dashboard"))

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
    st.markdown("### 3. AI-Generated Insights (Mock)")
    st.write("- High risk for hypertension complications.")
    st.write("- Suggests monitoring blood glucose weekly.")

st.sidebar.markdown("---")
st.sidebar.markdown("Built for Veritas One")
st.sidebar.markdown("BTG Health Consulting")
