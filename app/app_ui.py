import streamlit as st
import requests
import pandas as pd
import io

# Base URL of your FastAPI backend
API_URL = "http://127.0.0.1:8000"

st.title("🩺 Diabetes Prediction App")

# Session state for token
if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

# Sidebar: Register or Login form
with st.sidebar:
    st.header("🔐 Authentication")

    auth_mode = st.radio("Choose action", ["Login", "Register"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if auth_mode == "Register":
        name = st.text_input("Full Name")
        if st.button("Create Account"):
            if not (name and email and password):
                st.warning("Please fill in all fields.")
            else:
                response = requests.post(f"{API_URL}/users/register", json={
                    "name": name,
                    "email": email,
                    "password": password
                })
                if response.status_code == 200:
                    st.success("🎉 Account created! You can now log in.")
                else:
                    st.error(response.json().get("detail", "Registration failed."))

    elif auth_mode == "Login":
        if st.button("Login"):
            if not (email and password):
                st.warning("Please enter both email and password.")
            else:
                response = requests.post(f"{API_URL}/users/login", json={
                    "email": email,
                    "password": password
                })
                if response.status_code == 200:
                    st.session_state["access_token"] = response.json()["access_token"]
                    st.success("✅ Login successful!")
                else:
                    st.error("Invalid email or password.")

# ✅ After login
if st.session_state["access_token"]:
    st.success("✅ Logged in!")

    uploaded_file = st.file_uploader("📤 Upload your CSV file for prediction", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("📄 Uploaded Data Preview:")
        st.dataframe(df)

        if st.button("🔍 Predict"):
            headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
            response = requests.post(f"{API_URL}/ml/predict", headers=headers, files=files)
            
            if response.status_code == 200:
                predictions = response.json()["predictions"]
                result_df = pd.DataFrame(predictions)
                st.success("🎯 Prediction Results:")
                st.dataframe(result_df)

                # ✅ Download results as CSV
                csv_buffer = io.StringIO()
                result_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="⬇️ Download Results as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="prediction_results.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"Prediction failed: {response.text}")

    # ✅ View prediction history button
    if st.button("📜 View Prediction History"):
        headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
        response = requests.get(f"{API_URL}/ml/history", headers=headers)

        if response.status_code == 200:
            history_data = response.json()["history"]
            history_df = pd.DataFrame(history_data)
            st.info("📂 Past Predictions:")
            st.dataframe(history_df)
        else:
            st.error("Could not load prediction history.")
else:
    st.warning("🔐 Please log in to access features.")