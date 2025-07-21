import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Hardcoded configuration
EMAIL_ADDRESS = "smooosh.app@gmail.com"
# For security, you should use Streamlit secrets for the password in production
EMAIL_PASSWORD = "gqps twpm nytm eupg"  # Your Gmail app password

# Recipient details
RECIPIENTS = {
    "Osher": {
        "email": "osher@yshimoni.com",
        "sender_name": "Toria"    # Who the message is from when Osher is recipient
    },
    "Toria": {
        "email": "victoriaann001@gmail.com",
        "sender_name": "Osher"    # Who the message is from when Toria is recipient
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
            recipient_email = recipient["email"]
            sender_name = recipient["sender_name"]
            
            # Use custom message if provided, otherwise use default
            if use_custom_message and custom_message.strip():
                message_text = custom_message
            else:
                message_text = f"{sender_name} just sent you a smoosh! SMOOOOOSH"
            
            # Create HTML message with better formatting
            msg = MIMEMultipart("alternative")
            msg['From'] = f"Smoosh App <{EMAIL_ADDRESS}>"
            msg['To'] = recipient_email
            msg['Subject'] = f"SMOOSH from {sender_name}! 💕"
            
            # Plain text version
            text_part = MIMEText(message_text, "plain")
            
            # HTML version with styling
            html_content = f"""
            <html>
              <head>
                <style>
                  body {{ font-family: Arial, sans-serif; }}
                  .container {{ padding: 20px; max-width: 600px; margin: 0 auto; }}
                  .message {{ font-size: 18px; color: #333; }}
                  .signature {{ margin-top: 30px; color: #777; font-size: 14px; }}
                </style>
              </head>
              <body>
                <div class="container">
                  <div class="message">
                    {message_text}
                  </div>
                  <div class="signature">
                    Sent from the Smoosh App<br>
                    <small>This is an automated message. Please add smooosh.app@gmail.com to your contacts to ensure delivery.</small>
                  </div>
                </div>
              </body>
            </html>
            """
            html_part = MIMEText(html_content, "html")
            
            # Add both parts to the message
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Add headers to improve deliverability
            msg.add_header('List-Unsubscribe', f'<mailto:{EMAIL_ADDRESS}?subject=unsubscribe>')
            
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
            
            st.success(f"Smoosh sent successfully to {recipient_name}! 🎉")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error sending smoosh: {str(e)}")

# Add instructions for recipients
st.markdown("---")
st.subheader("For Recipients: How to Ensure You Receive Smooshes")
st.markdown("""
To make sure you always receive Smoosh notifications:

1. Add **smooosh.app@gmail.com** to your contacts
2. If you find a Smoosh email in your spam folder:
   - Mark it as "Not Spam"
   - Move it to your inbox
3. Create a filter to always allow emails from Smoosh App:
   - In Gmail, click the gear icon ⚙️ > See all settings
   - Go to "Filters and Blocked Addresses" tab
   - Click "Create a new filter"
   - Enter "smooosh.app@gmail.com" in the "From" field
   - Click "Create filter"
   - Check "Never send it to Spam" and "Always mark it as important"
   - Click "Create filter"
""")
