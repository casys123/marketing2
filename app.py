import streamlit as st
import pandas as pd
import openai
import requests
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from validate_email_address import validate_email
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Miami Master Flooring - Email Marketing App")

# --- Language Toggle ---
language = st.radio("Choose Language for Email Generation", ["English", "Spanish"])

# --- Lead Entry ---
st.header("1. Lead Entry")
with st.form("lead_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    address = st.text_input("Business Address")
    submit_lead = st.form_submit_button("Add Lead")

if "leads" not in st.session_state:
    st.session_state.leads = []

if submit_lead:
    if validate_email(email) and email not in [l['Email'] for l in st.session_state.leads]:
        st.session_state.leads.append({
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Address": address
        })
        pd.DataFrame(st.session_state.leads).to_csv("leads.csv", index=False)
        st.success("Lead added successfully.")
    else:
        st.error("Invalid or duplicate email address.")

# --- Display Leads ---
st.header("2. Current Lead List")
if st.session_state.leads:
    df_leads = pd.DataFrame(st.session_state.leads)
    st.dataframe(df_leads)
    st.download_button("Download Lead List as CSV", df_leads.to_csv(index=False), "leads.csv")

# --- Generate Email ---
st.header("3. Generate Email Template with ChatGPT")
subject = st.text_input("Email Subject")
prompt = st.text_area("Describe the purpose of the email (e.g., promo, intro, follow-up)")
image = st.file_uploader("Upload Image to Embed in Email", type=["png", "jpg", "jpeg"])
if st.button("Generate Email"):
    if prompt:
        lang_instruction = "Write in Spanish." if language == "Spanish" else "Write in English."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"{lang_instruction} Write a persuasive marketing email for Miami Master Flooring. Purpose: {prompt}"}
            ]
        )
        email_body = response.choices[0].message['content']
        st.markdown("### Generated Email:")
        st.write(email_body)

        if image:
            img_bytes = image.read()
            img_b64 = base64.b64encode(img_bytes).decode('utf-8')
            img_html = f'<br><img src="data:image/png;base64,{img_b64}" width="400" />'
            email_body += img_html

        st.session_state.generated_email = {
            "subject": subject,
            "body": email_body,
            "image": image.name if image else None,
            "image_data": img_bytes if image else None
        }
    else:
        st.warning("Please enter a prompt to generate the email.")

# --- Schedule Emails ---
st.header("4. Schedule Emails")
frequency = st.selectbox("Email Frequency", ["1x per week", "2x per week", "3x per week"])
scheduled_day = st.date_input("Start Date", datetime.today())
if st.button("Confirm Schedule"):
    times_per_week = int(frequency[0])
    st.success(f"Scheduled to send {times_per_week} times per week starting {scheduled_day}.")

# --- Send Test Email ---
st.header("5. Send Test Email (Simulation)")
sender_email = st.text_input("Your Email (for SMTP)")
receiver_email = st.text_input("Send Test Email To")
email_password = st.text_input("Your Email Password", type="password")
if st.button("Send Test Email"):
    if "generated_email" in st.session_state:
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = st.session_state.generated_email['subject']

            body = MIMEText(st.session_state.generated_email['body'], 'html')
            msg.attach(body)

            if st.session_state.generated_email.get("image_data"):
                img = MIMEImage(st.session_state.generated_email["image_data"])
                img.add_header('Content-ID', '<image1>')
                msg.attach(img)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, email_password)
                server.send_message(msg)

            st.success("Test email sent successfully.")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
    else:
        st.warning("Generate an email before sending.")
