# marketing2 app.py

import streamlit as st
import pandas as pd
import openai
import requests
import base64
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from validate_email_address import validate_email
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
gmaps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

st.set_page_config(page_title="Marketing2 App", layout="wide")
st.title("Miami Master Flooring - Marketing System")

# --- Session State Setup ---
if "leads" not in st.session_state:
    st.session_state.leads = []
if "sent_logs" not in st.session_state:
    st.session_state.sent_logs = []

# --- Lead Entry Section ---
st.header("1. Manual Lead Entry")
with st.form("lead_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    address = st.text_input("Business Address")
    submit_lead = st.form_submit_button("Add Lead")

if submit_lead:
    if validate_email(email) and email not in [l['Email'] for l in st.session_state.leads]:
        st.session_state.leads.append({"Name": name, "Email": email, "Phone": phone, "Address": address})
        st.success("Lead added successfully.")
    else:
        st.error("Invalid or duplicate email address.")

# --- Google Places Search ---
st.header("2. Business Search (Google Places)")
search_type = st.text_input("Search for...", placeholder="e.g., General Contractor")
location = st.text_input("City or Zip Code", value="Miami, FL")
if st.button("Search Google Places") and gmaps_api_key:
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_type}+in+{location}&key={gmaps_api_key}"
    res = requests.get(url).json()
    for place in res.get("results", []):
        name = place.get("name")
        address = place.get("formatted_address")
        phone = place.get("formatted_phone_number", "")
        st.write(f"**{name}** - {address}")
        if st.button(f"Add {name}", key=name):
            st.session_state.leads.append({"Name": name, "Email": "", "Phone": phone, "Address": address})

# --- Lead Table ---
st.header("3. Current Leads")
if st.session_state.leads:
    df_leads = pd.DataFrame(st.session_state.leads)
    st.dataframe(df_leads)
    st.download_button("Download Leads CSV", df_leads.to_csv(index=False), "leads.csv")

# --- Email Template Generator ---
st.header("4. Email Templates & Generator")
language = st.radio("Choose Email Language", ["English", "Spanish"])
template_choice = None

# Load templates
if os.path.exists("templates.json"):
    with open("templates.json") as f:
        templates = json.load(f)
    options = [t['name'] for t in templates]
    template_choice = st.selectbox("Choose a Template", options)
    selected_template = next((t for t in templates if t['name'] == template_choice), None)
else:
    st.warning("No templates.json found")

subject = st.text_input("Email Subject", value=selected_template['subject'] if selected_template else "")
prompt = st.text_area("Custom Purpose or Prompt")
if st.button("Generate Email"):
    if prompt or selected_template:
        context = f"Write in {language}. Purpose: {prompt}" if prompt else selected_template['body']
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": context}]
        )
        email_body = response.choices[0].message['content']
        st.markdown("### Generated Email:")
        st.write(email_body)
        st.session_state.generated_email = {"subject": subject, "body": email_body}

# --- Campaign Scheduler ---
st.header("5. Schedule Campaign (Manual Simulation)")
frequency = st.selectbox("Email Frequency", ["1x/week", "2x/week", "3x/week"])
scheduled_day = st.date_input("Start Date", datetime.today())

if st.button("Simulate Send") and "generated_email" in st.session_state:
    for lead in st.session_state.leads:
        log = {
            "To": lead['Email'],
            "Subject": st.session_state.generated_email['subject'],
            "Date": str(datetime.now())
        }
        st.session_state.sent_logs.append(log)
    st.success(f"Simulated sending to {len(st.session_state.leads)} leads")

# --- Sent Log ---
st.header("6. Sent Email Log")
if st.session_state.sent_logs:
    df_logs = pd.DataFrame(st.session_state.sent_logs)
    st.dataframe(df_logs)
    st.download_button("Download Sent Log", df_logs.to_csv(index=False), "sent_log.csv")
