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

# Helper function to load contacts from CSV
def load_contacts():
    try:
        return pd.read_csv("contacts.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Email", "Company", "Phone", "Business Type", "Location", "Status", "Source"])

# Helper function to save contacts to CSV
def save_contacts(df):
    df.to_csv("contacts.csv", index=False)

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
    st.text_input("Search contacts, campaigns...")
    st.button("New Campaign")

    contacts_df = load_contacts()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Contacts", str(len(contacts_df)), "+12% from last month")
    col2.metric("Emails Sent", "0", "+8% from last week")
    col3.metric("Open Rate", "0%", "-2% from last month")
    col4.metric("Active Campaigns", "0")

    st.subheader("Recent Campaigns")
    st.markdown("**South Florida Architects Partnership Outreach**\nDraft • 0 recipients selected")
    st.markdown("**BC63125**\nDraft • 0 recipients selected")
    st.markdown("**gc-miami-73125**\nDraft • 0 recipients selected")

elif menu == "Contacts":
    st.title("Contacts")
    st.subheader("Manage your email marketing contacts")

    df = load_contacts()

    if st.button("Export CSV"):
        st.download_button("Download Contacts", data=df.to_csv(index=False), file_name="contacts.csv")

    uploaded_file = st.file_uploader("Import CSV")
    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        df = pd.concat([df, df_uploaded], ignore_index=True).drop_duplicates()
        save_contacts(df)
        st.success("Contacts imported successfully.")

    if st.button("Add Contact"):
        with st.form("add_contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            company = st.text_input("Company")
            phone = st.text_input("Phone")
            business_type = st.text_input("Business Type")
            location = st.text_input("Location")
            submitted = st.form_submit_button("Save")
            if submitted:
                df.loc[len(df)] = [name, email, company, phone, business_type, location, "pending", "manual"]
                save_contacts(df)
                st.success("Contact added.")

    st.text_input("Search contacts...")
    st.selectbox("Filter", [f"All Contacts ({len(df)})"])
    st.dataframe(df, use_container_width=True)

elif menu == "Lead Generation":
    st.title("Lead Generation")
    st.subheader("Find and extract business contacts using Google Search")
    st.text_input("Business Type", "e.g., general contractors")
    st.text_input("Location", "e.g., Miami-Dade County")
    st.button("Search Leads")
    st.markdown("**Quick Actions**")
    st.button("Create AI Template")
    st.button("Import Contacts")
    st.button("Validate Emails")
    st.button("Schedule Campaign")

elif menu == "Email Templates":
    st.title("Email Templates")
    st.subheader("Create and manage your email marketing templates")
    st.button("Create Template")
    st.text_input("Search templates...")
    st.selectbox("Filter", ["All", "General", "Follow_up", "Promotion", "Welcome"])

    st.markdown("**Welcome New Lead**\nThanks for your interest! Let's discuss your project\n\n**welcome**\n**professional**\nUsed 0 times\n0.00% avg open rate")
    st.button("Edit")
