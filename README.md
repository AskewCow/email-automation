# 📧 Email Automation Tool

A powerful, flexible Python script for sending personalized HTML emails with scheduling capabilities. Perfect for academic research, surveys, marketing campaigns, and professional outreach.

## ✨ Features

-   🎨 **Personalized HTML Emails** - Use templates with dynamic placeholders
-   📅 **Smart Scheduling** - Send emails at specific times or dates
-   🧪 **Safe Testing** - Dry run mode to test without sending
-   📝 **Comprehensive Logging** - Console output with colors + optional file logging
-   🔒 **Secure Configuration** - Environment variables for sensitive data
-   📤 **BCC Support** - Add blind carbon copy recipients
-   🔄 **Batch Processing** - Handle multiple recipient groups efficiently
-   🛡️ **Error Handling** - Robust error handling with clear messages

## 🚀 Quick Start

### 1. **Clone & Setup**

```bash
git clone https://github.com/YourUsername/email-automation.git
cd email-automation
pip install -r requirements.txt
```

### 2. **Configure Environment**

Copy the example configuration:

```bash
cp .env.example .env
```

Edit `.env` with your details:

```bash
# Email Configuration
YOUR_EMAIL=your_email@gmail.com
YOUR_PASSWORD=your_app_password_here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

# Email Content
SUBJECT_LINE=🌟 Your Custom Subject Line
SENDER_NAME=Your Name
AFFILIATION=Your Organization
BCC_EMAILS=supervisor@example.com,backup@example.com

# Safety & Logging
DRY_RUN=true
LOG_TO_FILE=true

# Scheduling (optional)
SEND_AT=14:30
# SEND_AT=2025-07-22 09:00
```

### 3. **Prepare Recipients**

Create `email_recipients.json`:

```json
[
    {
        "university": "Trinity College Dublin",
        "emails": ["contact@tcd.ie", "admin@tcd.ie"]
    },
    {
        "university": "University College Dublin",
        "emails": ["info@ucd.ie"]
    }
]
```

### 4. **Test & Send**

```bash
# Test first (DRY_RUN=true)
python send_emails.py

# Send for real (DRY_RUN=false)
python send_emails.py
```

## 📋 Detailed Setup Guide

### 🔐 Email Authentication Setup

#### **Gmail with 2FA (Recommended)**

1. **Enable 2-Factor Authentication** in your Google Account
2. **Generate App Password**:
    - Go to [Google Account Security](https://myaccount.google.com/security)
    - Navigate: Security → 2-Step Verification → App passwords
    - Select "Mail" and generate password
    - Use the 16-character password in your `.env` file

#### **Other Email Providers**

| Provider    | SMTP Server           | Port   | Authentication        |
| ----------- | --------------------- | ------ | --------------------- |
| **Gmail**   | `smtp.gmail.com`      | `465`  | App Password (if 2FA) |
| **Outlook** | `smtp.live.com`       | `587`  | App Password          |
| **Yahoo**   | `smtp.mail.yahoo.com` | `465`  | App Password          |
| **Custom**  | Your server           | Varies | Regular/App Password  |

### 📁 File Structure

```
email-automation/
├── send_emails.py          # Main script
├── email_template.html     # Your HTML template
├── email_recipients.json   # Recipient data
├── requirements.txt        # Python dependencies
├── .env                   # Your configuration (create this)
├── .env.example          # Configuration template
├── log.txt               # Generated log file (optional)
└── README.md            # This file
```

### 🎨 HTML Template Format

Your `email_template.html` should include these placeholders:

```html
<!DOCTYPE html>
<html>
    <body>
        <h2>Dear {{Recipient Department/Office}},</h2>

        <p>Your email content here...</p>

        <p>
            Sincerely,<br />
            {{Your Name/Project Name}}<br />
            {{Your Affiliation/Study Area}}
        </p>
    </body>
</html>
```

**Placeholders:**

-   `{{Recipient Department/Office}}` → Replaced with `university` from JSON
-   `{{Your Name/Project Name}}` → Replaced with `SENDER_NAME` from .env
-   `{{Your Affiliation/Study Area}}` → Replaced with `AFFILIATION` from .env

## ⚙️ Configuration Options

### 📧 **Email Settings**

```bash
YOUR_EMAIL=your_email@gmail.com          # Your sending email
YOUR_PASSWORD=app_password_here          # App password (not regular password!)
SMTP_SERVER=smtp.gmail.com              # Email provider's SMTP server
SMTP_PORT=465                           # SMTP port (465 for SSL, 587 for TLS)
```

### 📝 **Content Settings**

```bash
SUBJECT_LINE=Your Email Subject          # Email subject line
SENDER_NAME=Your Full Name              # Your name in email signature
AFFILIATION=Your Organization           # Your organization/department
BCC_EMAILS=email1@ex.com,email2@ex.com # Comma-separated BCC recipients
```

### 📂 **File Settings**

```bash
HTML_TEMPLATE_FILE=email_template.html  # Path to HTML template
JSON_FILE=email_recipients.json         # Path to recipients JSON
LOG_FILE=log.txt                        # Log file path
```

### 🧪 **Testing & Logging**

```bash
DRY_RUN=true                            # Test mode (true/false)
LOG_TO_FILE=true                        # Save logs to file (true/false)
```

### ⏰ **Scheduling**

```bash
SEND_AT=                                # Send immediately (empty)
SEND_AT=14:30                           # Send today at 2:30 PM
SEND_AT=2025-07-22 09:00               # Send on specific date/time
```

## 🎯 Usage Examples

### **Example 1: Immediate Send**

```bash
# .env settings
DRY_RUN=false
SEND_AT=
```

### **Example 2: Schedule for Later Today**

```bash
# .env settings
SEND_AT=15:30                           # Send at 3:30 PM today
```

### **Example 3: Schedule for Future Date**

```bash
# .env settings
SEND_AT=2025-07-25 09:00               # Send on July 25th at 9 AM
```

### **Example 4: Test Campaign**

```bash
# .env settings
DRY_RUN=true                           # Safe testing mode
LOG_TO_FILE=true                       # Save detailed logs
```

## 🔍 Understanding the Output

The script provides colorized console output:

```
🚀 EMAIL AUTOMATION SCRIPT STARTED
══════════════════════════════════════════════════════════

ℹ️  📧 Sender: your_email@gmail.com
ℹ️  📄 Template: email_template.html
ℹ️  📂 Recipients: email_recipients.json
⚠️  🧪 DRY RUN MODE: No emails will be sent!

📨 STARTING EMAIL CAMPAIGN
══════════════════════════════════════════════════════════

🏫 📍 Processing Trinity College Dublin (2 emails)
✅ ✉️  Sent to: contact@tcd.ie
✅ ✉️  Sent to: admin@tcd.ie

📈 CAMPAIGN SUMMARY
══════════════════════════════════════════════════════════
✅ 📧 Successfully sent: 2
✅ ✅ Total processed: 2
⚠️  🧪 This was a DRY RUN - no actual emails were sent
```

## 🛡️ Security Best Practices

### ✅ **DO:**

-   ✅ Use App Passwords for 2FA-enabled accounts
-   ✅ Keep `.env` file out of version control (it's in `.gitignore`)
-   ✅ Test with `DRY_RUN=true` first
-   ✅ Use BCC for sensitive recipient lists
-   ✅ Review logs before and after sending

### ❌ **DON'T:**

-   ❌ Use your regular email password with 2FA enabled
-   ❌ Commit `.env` file to Git
-   ❌ Send to large lists without testing first
-   ❌ Include sensitive data in recipient JSON if sharing

## 🔧 Troubleshooting

### **"Authentication Failed" Error**

-   ✅ Verify you're using an App Password (not regular password)
-   ✅ Check SMTP server and port are correct
-   ✅ Ensure 2FA is enabled and App Password is generated

### **"File Not Found" Error**

-   ✅ Check file paths in `.env` are correct
-   ✅ Ensure `email_template.html` and `email_recipients.json` exist
-   ✅ Verify you're running script from correct directory

### **"Invalid JSON" Error**

-   ✅ Validate JSON syntax using online JSON validator
-   ✅ Check for trailing commas or missing quotes
-   ✅ Ensure UTF-8 encoding

### **Scheduling Not Working**

-   ✅ Use correct format: `HH:MM` or `YYYY-MM-DD HH:MM`
-   ✅ Keep terminal/command prompt open during scheduled wait
-   ✅ Ensure computer doesn't sleep during wait time

## 📊 Advanced Features

### **Logging**

Enable file logging for detailed records:

```bash
LOG_TO_FILE=true
LOG_FILE=campaign_2025_07_21.log
```

### **Multiple BCC Recipients**

Add multiple supervisors or monitoring emails:

```bash
BCC_EMAILS=supervisor@uni.edu,backup@org.com,monitor@dept.edu
```

### **Custom File Locations**

Organize your files:

```bash
HTML_TEMPLATE_FILE=templates/survey_invitation.html
JSON_FILE=data/research_participants.json
LOG_FILE=logs/campaign_$(date).log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Enable logging** (`LOG_TO_FILE=true`) for detailed error information
3. **Test in DRY_RUN mode** to isolate issues
4. **Open an issue** with:
    - Error messages (remove sensitive data)
    - Your configuration (remove credentials)
    - Steps to reproduce

---

**Made with ❤️ for efficient email automation**
