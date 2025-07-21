import os
import json
import smtplib
from email.message import EmailMessage
import ssl
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

load_dotenv()

# Color codes for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE, emoji=""):
    """Print colored message with optional emoji"""
    print(f"{color}{emoji} {message}{Colors.END}")

def print_header(message):
    """Print a formatted header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(message):
    """Print success message in green"""
    print_colored(message, Colors.GREEN, "✅")

def print_error(message):
    """Print error message in red"""
    print_colored(message, Colors.RED, "❌")

def print_warning(message):
    """Print warning message in yellow"""
    print_colored(message, Colors.YELLOW, "⚠️")

def print_info(message):
    """Print info message in blue"""
    print_colored(message, Colors.BLUE, "ℹ️")

def print_progress(message):
    """Print progress message in magenta"""
    print_colored(message, Colors.MAGENTA, "⏳")

def validate_required_env_vars():
    """Validate that required environment variables are set."""
    required_vars = ["YOUR_EMAIL", "YOUR_PASSWORD"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print_error(f"Missing required environment variables: {', '.join(missing_vars)}")
        print_warning("Please set them in your .env file.")
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. "
                        f"Please set them in your .env file.")

# Validate required environment variables
validate_required_env_vars()

# File Configuration
JSON_FILE = os.getenv("JSON_FILE", "email_recipients.json")
HTML_TEMPLATE_FILE = os.getenv("HTML_TEMPLATE_FILE", "email_template.html")

# Email Configuration
YOUR_EMAIL = os.getenv("YOUR_EMAIL")
YOUR_PASSWORD = os.getenv("YOUR_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

# Email Content Configuration
SUBJECT_LINE = os.getenv("SUBJECT_LINE", "Subject Not Set")
SENDER_NAME = os.getenv("SENDER_NAME", "Your Name")
AFFILIATION = os.getenv("AFFILIATION", "Your Affiliation")
BCC_EMAILS = os.getenv("BCC_EMAILS", "")

# Testing and Logging Configuration
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "false").lower() == "true"
LOG_FILE = os.getenv("LOG_FILE", "log.txt")

# Scheduling Configuration
SEND_AT = os.getenv("SEND_AT", "")

def log_message(message, level="INFO"):
    """Log message to console and optionally to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {level}: {message}"
    
    # Console output with colors
    if level == "SUCCESS":
        print_success(message)
    elif level == "ERROR":
        print_error(message)
    elif level == "WARNING":
        print_warning(message)
    elif level == "PROGRESS":
        print_progress(message)
    else:
        print_info(message)
    
    # File logging
    if LOG_TO_FILE:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as log_file:
                log_file.write(formatted_message + "\n")
        except Exception as e:
            print_error(f"Failed to write to log file: {e}")

def parse_scheduled_time(send_at_str):
    """Parse the SEND_AT string and return a datetime object"""
    if not send_at_str.strip():
        return None
    
    try:
        current_time = datetime.now()
        
        # Check if it's just time (HH:MM) - assume today
        if ":" in send_at_str and "-" not in send_at_str:
            time_parts = send_at_str.strip().split(":")
            hour = int(time_parts[0])
            minute = int(time_parts[1])
            
            scheduled_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time has already passed today, schedule for tomorrow
            if scheduled_time <= current_time:
                scheduled_time += timedelta(days=1)
                log_message(f"Scheduled time has passed today, scheduling for tomorrow: {scheduled_time.strftime('%Y-%m-%d %H:%M')}", "WARNING")
            
            return scheduled_time
        
        # Full datetime format (YYYY-MM-DD HH:MM)
        else:
            return datetime.strptime(send_at_str.strip(), "%Y-%m-%d %H:%M")
    
    except ValueError as e:
        print_error(f"Invalid SEND_AT format: {send_at_str}")
        print_info("Use format: 'HH:MM' for today or 'YYYY-MM-DD HH:MM' for specific date")
        raise ValueError(f"Invalid SEND_AT format: {send_at_str}. Use 'HH:MM' or 'YYYY-MM-DD HH:MM'")

def wait_until_scheduled_time(scheduled_time):
    """Wait until the scheduled time, showing countdown"""
    if not scheduled_time:
        return
    
    print_header(f"📅 EMAIL SCHEDULED FOR: {scheduled_time.strftime('%A, %B %d, %Y at %H:%M')}")
    
    while True:
        current_time = datetime.now()
        if current_time >= scheduled_time:
            print_success("⏰ Scheduled time reached! Starting email sending process...")
            break
        
        time_diff = scheduled_time - current_time
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if time_diff.days > 0:
            print_progress(f"⏱️  Waiting... {time_diff.days} day(s), {hours:02d}:{minutes:02d}:{seconds:02d} remaining")
        else:
            print_progress(f"⏱️  Waiting... {hours:02d}:{minutes:02d}:{seconds:02d} remaining")
        
        time.sleep(5)  # Update every 5 seconds

def load_recipients():
    """Load recipient data from JSON file"""
    try:
        print_info(f"📂 Loading recipients from: {JSON_FILE}")
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            recipients = json.load(file)
        print_success(f"📊 Loaded {len(recipients)} recipient group(s)")
        return recipients
    except FileNotFoundError:
        print_error(f"📂 File not found: {JSON_FILE}")
        raise
    except json.JSONDecodeError:
        print_error(f"📂 Invalid JSON format in: {JSON_FILE}")
        raise

def load_html_template():
    """Load HTML email template"""
    try:
        print_info(f"📄 Loading email template: {HTML_TEMPLATE_FILE}")
        with open(HTML_TEMPLATE_FILE, 'r', encoding='utf-8') as file:
            template = file.read()
        print_success("📄 Email template loaded successfully")
        return template
    except FileNotFoundError:
        print_error(f"📄 Template file not found: {HTML_TEMPLATE_FILE}")
        raise

def send_email(to_email, subject, html_content, bcc_list=None):
    """Send an individual email"""
    try:
        # Create message
        msg = EmailMessage()
        msg['From'] = YOUR_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if bcc_list:
            msg['Bcc'] = ', '.join(bcc_list)
        
        msg.set_content(html_content, subtype='html')
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(YOUR_EMAIL, YOUR_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print_error(f"Failed to send email to {to_email}: {str(e)}")
        return False

def main():
    """Main function to coordinate email sending"""
    print_header("🚀 EMAIL AUTOMATION SCRIPT STARTED")
    
    # Display configuration
    print_info(f"📧 Sender: {YOUR_EMAIL}")
    print_info(f"📄 Template: {HTML_TEMPLATE_FILE}")
    print_info(f"📂 Recipients: {JSON_FILE}")
    print_info(f"📝 Subject: {SUBJECT_LINE}")
    print_info(f"👤 Sender Name: {SENDER_NAME}")
    print_info(f"🏫 Affiliation: {AFFILIATION}")
    
    if DRY_RUN:
        print_warning("🧪 DRY RUN MODE: No emails will be sent!")
    
    if LOG_TO_FILE:
        print_info(f"📋 Logging to file: {LOG_FILE}")
    
    # Handle scheduling
    if SEND_AT:
        try:
            scheduled_time = parse_scheduled_time(SEND_AT)
            if scheduled_time:
                wait_until_scheduled_time(scheduled_time)
        except ValueError:
            return
    else:
        print_info("⚡ Sending emails immediately")
    
    # Load data
    try:
        recipients_data = load_recipients()
        html_template = load_html_template()
    except Exception as e:
        log_message(f"Failed to load required files: {e}", "ERROR")
        return
    
    # Prepare BCC list
    bcc_list = []
    if BCC_EMAILS:
        bcc_list = [email.strip() for email in BCC_EMAILS.split(',') if email.strip()]
        print_info(f"📤 BCC recipients: {len(bcc_list)}")
    
    # Send emails
    print_header("📨 STARTING EMAIL CAMPAIGN")
    
    total_emails = sum(len(group['emails']) for group in recipients_data)
    sent_count = 0
    failed_count = 0
    
    print_info(f"📊 Total emails to send: {total_emails}")
    
    for group in recipients_data:
        university = group['university']
        emails = group['emails']
        
        print_colored(f"\n📍 Processing {university} ({len(emails)} emails)", Colors.CYAN, "🏫")
        
        for email in emails:
            # Personalize template
            personalized_html = html_template.replace('{{Recipient Department/Office}}', university)
            personalized_html = personalized_html.replace('{{Your Name/Project Name}}', SENDER_NAME)
            personalized_html = personalized_html.replace('{{Your Affiliation/Study Area}}', AFFILIATION)
            
            if DRY_RUN:
                print_colored(f"[DRY RUN] Would send to: {email}", Colors.YELLOW, "🧪")
                sent_count += 1
            else:
                if send_email(email, SUBJECT_LINE, personalized_html, bcc_list):
                    print_success(f"✉️  Sent to: {email}")
                    sent_count += 1
                else:
                    failed_count += 1
                
                # Small delay between emails
                time.sleep(1)
    
    # Final summary
    print_header("📈 CAMPAIGN SUMMARY")
    print_success(f"📧 Successfully sent: {sent_count}")
    if failed_count > 0:
        print_error(f"❌ Failed to send: {failed_count}")
    print_success(f"✅ Total processed: {sent_count + failed_count}")
    
    if DRY_RUN:
        print_warning("🧪 This was a DRY RUN - no actual emails were sent")
        print_info("💡 Set DRY_RUN=false in .env to send real emails")
    
    log_message(f"Email campaign completed. Sent: {sent_count}, Failed: {failed_count}", "SUCCESS")

if __name__ == "__main__":
    main()
