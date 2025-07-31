# marketing2 app.py

import streamlit as st
import pandas as pd
import openai
import requests
import base64
import smtplib
import json
import re
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

st.set_page_config(page_title="EmailMarketer Pro", layout="wide")

# Sidebar Navigation
menu = st.sidebar.radio("", [
    "Dashboard", "Contacts", "Lead Generation", "Email Templates", "Campaigns", "Analytics", "API Config", "Settings"
])
st.sidebar.markdown("---")
st.sidebar.markdown("**John Doe**")
st.sidebar.markdown("Premium Plan")

if menu == "Dashboard":
    st.title("Dashboard")
    st.subheader("Manage your email marketing campaigns")
    st.text_input("Search contacts, campaigns...", key="search_dashboard")
    st.button("New Campaign")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Contacts", "29", "+12%")
    col2.metric("Emails Sent", "0", "+8%")
    col3.metric("Open Rate", "0%", "-2%")
    col4.metric("Active Campaigns", "0")

    st.subheader("Recent Campaigns")
    st.markdown("**South Florida Architects Partnership Outreach**\nDraft • 0 recipients selected")
    st.markdown("**BC63125**\nDraft • 0 recipients selected")
    st.markdown("**gc-miami-73125**\nDraft • 0 recipients selected")

elif menu == "Lead Generation":
    st.title("Lead Generation")
    st.subheader("Find and extract business contacts using Google Search")
    search_type = st.text_input("Business Type", placeholder="e.g., general contractors")
    location = st.text_input("Location", placeholder="e.g., Miami-Dade County")
    if st.button("Search Leads") and gmaps_api_key:
        text_search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={search_type}+in+{location}&key={gmaps_api_key}"
        response = requests.get(text_search_url).json()

        st.markdown(f"**API Status:** {response.get('status')}")
        if "error_message" in response:
            st.markdown(f"**Error:** {response['error_message']}")

        if response.get("results"):
            results = []
            for place in response["results"]:
                name = place.get("name")
                address = place.get("formatted_address")
                place_id = place.get("place_id")
                details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,formatted_phone_number,website&key={gmaps_api_key}"
                details = requests.get(details_url).json()
                result = details.get("result", {})
                phone = result.get("formatted_phone_number", "")
                email = ""

                website = result.get("website")
                if website:
                    try:
                        html = requests.get(website, timeout=5).text
                        found_emails = list(set(re.findall(r"[\w\.-]+@[\w\.-]+", html)))
                        email = found_emails[0] if found_emails else ""
                    except:
                        email = ""

                lead_entry = {
                    "Name": name,
                    "Email": email,
                    "Company": name,
                    "Phone": phone,
                    "Business Type": search_type,
                    "Location": location,
                    "Status": "pending",
                    "Source": "google_search"
                }
                results.append(lead_entry)

            st.write("### Extracted Leads")
            df = pd.DataFrame(results)
            st.dataframe(df)
            st.download_button("Download CSV", df.to_csv(index=False), "leads.csv")

elif menu == "Email Templates":
    st.title("Template Library")
    st.subheader("Quick Actions")
    st.button("Create AI Template")
    st.button("Import Contacts")
    st.button("Validate Emails")
    st.button("Schedule Campaign")

    templates = [
        {"name": "Architect Outreach - Flooring Partnership", "category": "general template"},
        {"name": "Thank You & Testimonial Request", "category": "follow_up template"},
        {"name": "Special Offer - Limited Time", "category": "promotion template"}
    ]

    for template in templates:
        st.markdown(f"**{template['name']}**\n{template['category']}\nUsed 0 times\n0.00% avg open rate")

elif menu == "Contacts":
    st.title("Contacts")
    st.subheader("Manage your email marketing contacts")
    if "leads" not in st.session_state:
        st.session_state.leads = []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button("Export CSV", pd.DataFrame(st.session_state.leads).to_csv(index=False), "contacts.csv")
    with col2:
        st.file_uploader("Import CSV", type=["csv"])
    with col3:
        st.button("Add Contact")

    st.text_input("Search contacts...")
    st.selectbox("Filter", ["All Contacts (29)"])

    if st.session_state.leads:
        df = pd.DataFrame(st.session_state.leads)
        st.dataframe(df, use_container_width=True)

elif menu == "Campaigns":
    st.title("Campaigns")
    st.markdown("Coming soon...")

elif menu == "Analytics":
    st.title("Analytics")
    st.markdown("Coming soon...")

elif menu == "API Config":
    st.title("API Config")
    st.text("OPENAI_API_KEY and GOOGLE_MAPS_API_KEY loaded from secrets.")

elif menu == "Settings":
    st.title("Settings")
    st.markdown("User preferences and configuration.")
