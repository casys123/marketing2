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

if menu == "Analytics":
    st.title("Analytics")
    st.subheader("Track your email marketing performance and insights")

    st.selectbox("Time Range", ["Last 30 days"])
    st.button("Export Report")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Campaigns", "24")
    col2.metric("Emails Sent", "15,429")
    col3.metric("Avg. Open Rate", "24.8%", "Below average")
    col4.metric("Avg. Click Rate", "7.5%", "Above average")

    st.subheader("Campaign Performance")
    analytics_data = [
        ["Miami Contractors Outreach", "1/15/2024", 245, 70, 21, 3, "28.6%", "8.6%", "Good"],
        ["Broward Architects Follow-up", "1/12/2024", 189, 47, 14, 2, "24.9%", "7.4%", "Average"],
        ["Q4 Services Promotion", "1/10/2024", 1247, 287, 89, 18, "23.0%", "7.1%", "Average"]
    ]
    df = pd.DataFrame(analytics_data, columns=[
        "Campaign", "Sent Date", "Emails Sent", "Opens", "Clicks", "Bounces", "Open Rate", "Click Rate", "Performance"])
    st.dataframe(df, use_container_width=True)

    st.subheader("Key Insights")
    st.markdown("- **Best performing campaign**\n\n  \"Miami Contractors Outreach\" achieved 28.6% open rate, which is 3.8% above your average")
    st.markdown("- **Optimal send time**\n\n  Tuesday 10:00 AM shows highest engagement rates across your campaigns")
    st.markdown("- **Subject line impact**\n\n  Subject lines with 6-8 words show 15% higher open rates than longer alternatives")

    st.subheader("Recommendations")
    st.markdown("- **Increase Frequency**\n\n  Your engagement rates are strong. Consider increasing email frequency to 2-3 times per week.")
    st.markdown("- **Segment Audiences**\n\n  Create targeted segments based on business type to improve relevance and engagement.")
    st.markdown("- **A/B Test Subject Lines**\n\n  Test different subject line approaches to optimize open rates further.")

elif menu == "API Config":
    st.title("Dashboard")
    st.subheader("Manage your email marketing campaigns")
    st.text_input("Search contacts, campaigns...")
    st.button("New Campaign")

    st.title("API Configuration")
    st.subheader("Configure your API keys to enable all platform features")
    st.button("Refresh Status")

    st.markdown("To use the full features of this platform, you'll need API keys from external services. Contact the platform administrator to configure these services.")
    st.subheader("Overview")
    st.markdown("**Setup Guide**")
    st.markdown("**API Testing**")

    st.markdown("### Google Places API")
    st.markdown("- **Status:** Configured")
    st.markdown("- Finds authentic businesses with verified addresses, phone numbers, and websites")

    st.markdown("### Email Validation")
    st.markdown("- **Status:** Configured")
    st.markdown("- Free email validation using DNS/MX record checking and domain verification")

    st.markdown("### Email Delivery")
    st.markdown("- **Google Workspace:** Missing")
    st.markdown("- Using info@miamimasterflooring.com for professional email delivery")

    st.markdown("### AI Services")
    st.markdown("- **OpenAI API:** Configured")
    st.markdown("- AI-powered email template creation and content optimization")
