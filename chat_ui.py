import streamlit as st
import pandas as pd
import requests
import json
import os

# --- Configuration ---
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")  # Or hardcode for testing (not recommended)
ENDPOINT_URL = "https://adb-3502834182629975.15.azuredatabricks.net/serving-endpoints/my_own_chatbot/invocations"

# --- UI ---
st.title("💬 Ask the Chatbot")

user_query = st.text_area("Enter your question:", height=150, placeholder="e.g. What does a SUDS message mean?")

if st.button("Ask"):
    if not user_query.strip():
        st.warning("Please enter a question.")
    elif not DATABRICKS_TOKEN:
        st.error("DATABRICKS_TOKEN not found. Set it in your environment variables.")
    else:
        # --- Prepare Input as Expected ---
        input_df = pd.DataFrame({"query": [user_query]})
        payload = {"dataframe_split": input_df.to_dict(orient="split")}
        data_json = json.dumps(payload)

        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }

        # --- Call Endpoint ---
        with st.spinner("Fetching answer from model..."):
            response = requests.post(ENDPOINT_URL, headers=headers, data=data_json)

        # --- Handle Response ---
        if response.status_code == 200:
            result = response.json()
            st.success("✅ Answer:")
            st.write(result)
        else:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
