import os
import pandas as pd
import smtplib
from email.message import EmailMessage
import ssl
from dotenv import load_dotenv

load_dotenv()

# Excel File contains the name and emails. HTML File contains the email content.
EXCEL_FILE = "Email-List.xlsx"
HTML_TEMPLATE_FILE = "email_template.html"

# Details needed for the STMP.
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
BCC_EMAILS = [] # Add list of BCC emails if desired.
SENDER_NAME = "Example Name"

# Loading in the HTML Template.
with open(HTML_TEMPLATE_FILE, "r", encoding="utf-8") as f:
    html_template = f.read()

# Loading in the Excel file.
df = pd.read_excel(EXCEL_FILE)

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

for idx, row in df.iterrows():
    try:
        # Extract the title, first name and email.
        title = str(row["Title"]).strip()
        first_name = str(row["First Name"]).strip()
        email = str(row["Email"]).strip()

        # Customise HTML template title, name and sender name.
        personalised_html = (
            html_template
            .replace("{{title}}", title)
            .replace("{{first_name}}", first_name)
            .replace("{{sender_name}}", SENDER_NAME)
        )

        # Function call with success message to console.
        send_email(email, subject_line, personalised_html, bcc_list=BCC_EMAILS)
        print(f"[✓] Email sent to: {title} {first_name} <{email}>")

    except Exception as e:
        # Error message printed to console if one occurs.
        print(f"[!] Failed to send to {row.get('Email', 'N/A')}: {e}")
