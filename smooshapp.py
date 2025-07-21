import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Hardcoded configuration
EMAIL_ADDRESS = "oshersmusic@gmail.com"
# For security, you should use Streamlit secrets for the password in production
# This is just for demonstration purposes
EMAIL_PASSWORD = "slua zzrs cgag yagl"  # Replace with your Gmail app password

# Recipient details
RECIPIENTS = {
    "Osher": {
        "phone": "5088082203",
        "carrier": "@vzwpix.com",  # Verizon
        "sender_name": "Toria"    # Who the message is from when Osher is recipient
    },
    "Toria": {
        "phone": "8573377180",
        "carrier": "@vzwpix.com",  # T-Mobile
        "sender_name": "Osher"      # Who the message is from when Toria is recipient
    }
}

# App UI
st.title("Smoosh App")

# Create a container for consistent width
container = st.container()

# Interface with dropdown, custom message option, and button
with container:
    recipient_name = st.selectbox("Choose smooshee:", options=list(RECIPIENTS.keys()))
    
    # Add option to use custom message
    use_custom_message = st.checkbox("Use custom message")
    
    custom_message = ""
    if use_custom_message:
        custom_message = st.text_area("Enter your custom message:", "")
    
    # Add a small space for visual separation
    st.write("")
    
    if st.button("Smoosh"):
        try:
            # Get recipient details
            recipient = RECIPIENTS[recipient_name]
            recipient_email = recipient["phone"] + recipient["carrier"]
            sender_name = recipient["sender_name"]
            
            # Use custom message if provided, otherwise use default
            if use_custom_message and custom_message.strip():
                message_text = custom_message
            else:
                message_text = f"{sender_name} just sent you a smoosh! SMOOOOOSH"
            
            # Create message
            message = MIMEText(message_text)
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
