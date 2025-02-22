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
st.sidebar.title("Veritas One")
page = st.sidebar.radio("Navigation",
                        ["Home", "Register", "Dashboard", "Upload Data", "Earnings", "Data Privacy & Usage",
                         "Investor Demo"])

# Home Page
if page == "Home":
    st.title("Welcome to Veritas One")
    st.write("Manage and monetize your health data securely.")
    if image_path:
        st.image(image_path, use_column_width=True)
    st.markdown("### Get Started")
    st.button("Sign Up", on_click=lambda: st.experimental_set_query_params(page="Register"))
    st.button("Log In", on_click=lambda: st.experimental_set_query_params(page="Dashboard"))

# Data Privacy & Usage Page
elif page == "Data Privacy & Usage":
    st.title("How Your Health Data is Stored & Used")
    st.markdown("""
    At Veritas One, we use a **two-database system** to keep your identifiable and de-identified data separate.

    **1. Your Identifiable Data (Stored in a Secure Personal Health Record)**
    - **Stored in:** A HIPAA-compliant, secure personal health record.
    - **Usage:** Shared only with your consent for medical care or personalized health services.
    - **Who Can See It?** Only you and those you explicitly share it with.

    **2. Your De-Identified Data (Used for Medical Research & Insights)**
    - **Stored in:** A separate research database without any identifying information.
    - **Usage:** Helps improve medicine, public health, and clinical care.
    - **Who Can See It?** Researchers and analysts, but they never see personal identifiers.

    **Your Control, Your Choice**
    - **No Sharing:** Fully private, no compensation, storage fee may apply.
    - **Research Only:** De-identified data used for medical research (5% profit share).
    - **Research + Ads:** De-identified + limited identifiable data for health ads (15% profit share).
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

# Investor Demo Page
elif page == "Investor Demo":
    st.title("Investor Demo: Backend Simulation")
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
