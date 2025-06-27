import os
import json
import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv

load_dotenv()

# JSON File contains the Uni name and Emails. HTML File contains the email content.
JSON_FILE = "test_email.json"
HTML_TEMPLATE_FILE = "email_template.html"

# Details needed for the STMP.
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
BCC_EMAILS = [] # Add list of BCC emails if desired.
SENDER_NAME = "Example Name"
AFFILIATION = "CSB @ TCD"

# Loading in the HTML Template.
with open(HTML_TEMPLATE_FILE, "r", encoding="utf-8") as f:
    html_template = f.read()

# Loading in the JSON file.
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Function for sending the emails.
def send_email(recipient_email, subject, html_content, bcc_list=[]):
    msg = EmailMessage()
    msg["From"] = YOUR_EMAIL
    msg["To"] = recipient_email
    msg["Subject"] = subject
    if bcc_list:
        msg["Bcc"] = ", ".join(bcc_list)

    msg.set_content("This email requires an HTML viewer.")
    msg.add_alternative(html_content, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(YOUR_EMAIL, YOUR_PASSWORD)
        server.send_message(msg)

# Loop for sending the emails repeatedly.
subject_line = "🌟 You Deserve Recognition - Improving Trinity’s Exchange Programme"

# Extract the Uni name and list of related emails.
for entry in data:
    university = entry.get("university", "there")
    emails = entry.get("emails", [])

    # Loop through list of emails and send one by one using send_email function.
    for email in emails:
        try:
            # Customise HTML template with Uni name.
            personalised_html = (
                html_template
                .replace("{{Recipient Department/Office}}", university)  
                .replace("{{Your Name/Project Name}}", SENDER_NAME) # Could be added directly to the HTML file.
                .replace("{{Your Affiliation/Study Area}}", AFFILIATION)
            )

            # Function call with success message to console.
            send_email(email, subject_line, personalised_html, bcc_list=BCC_EMAILS)
            print(f"[✓] Email sent to: {university} <{email}>")

        except Exception as e:
            # Error message printed to console if one occurs.
            print(f"[!] Failed to send to {email} ({university}): {e}")