import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Hardcoded configuration
EMAIL_ADDRESS = "smooosh.app@gmail.com"
# For security, you should use Streamlit secrets for the password in production
# This is just for demonstration purposes
EMAIL_PASSWORD = "hxth vign lgoo utiv"  # Replace with your Gmail app password

# Recipient details
RECIPIENTS = {
    "Osher": {
        "phone": "5088082203",
        "carrier": "@vtext.com"  # Verizon
    },
    "Toria": {
        "phone": "8573377180",
        "carrier": "@tmomail.net"  # T-Mobile
    }
}

# App UI
st.title("Smoosh Notification App")

# Simple interface with just a dropdown and button
recipient_name = st.selectbox("Choose recipient:", options=list(RECIPIENTS.keys()))

if st.button("Smoosh", type="primary"):
    try:
        # Get recipient details
        recipient = RECIPIENTS[recipient_name]
        recipient_email = recipient["phone"] + recipient["carrier"]
        
        # Create a simple plain text message (no multipart)
        message = MIMEText("Osher just sent you a smoosh!")
        message['From'] = EMAIL_ADDRESS
        message['To'] = recipient_email
        message['Subject'] = ""  # Empty subject line
        
        # Send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient_email, message.as_string())
        
        st.success(f"Smoosh sent successfully to {recipient_name}! 🎉")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error sending smoosh: {str(e)}")