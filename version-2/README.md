## Version 2

This version was updated to use a JSON file rather than an Excel file. Nothing particularly wrong with the previous version, but the email list was provided in a different format this time. This version was used for sending emails to around 650 emails regarding a project still in progress. More to come in the near future.

This version uses:
* **JSON File**: For contact addresses and university names (`test_email.json`).
* **HTML File**: For the email template (`email_template.html`). It uses placeholders like `{{Recipient Department/Office}}`, `{{Your Name/Project Name}}` and `{{Your Affiliation/Study Area}}`.

### Files in this Version

* `send_emails.py`: The core Python script that handles reading the JSON file, populating the HTML template, and sending emails.
* `email_template.html`: The HTML template for your email.
* `requirements.txt`: Lists the Python dependency (`python-dotenv`).
* `.env`: (You will need to create this) Stores your sensitive email credentials. **This file is excluded from GitHub.**
* `test_email.json`: (You will create/provide this) Your JSON file containing recipient data. **This file should be excluded from GitHub if it contains sensitive data. The one present is simply for illustration purposes.**

### Quick Setup & Run

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/YourRepoName.git](https://github.com/YourUsername/YourRepoName.git)
    cd YourRepoName
    ```
    (Replace `YourUsername` and `YourRepoName` with your actual GitHub details.)

2.  **Install Dependencies:**
    It's highly recommended to use a virtual environment for dependency management (see "Recommended: Using a Virtual Environment" below). For a quick start, you can install globally:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare `test_email.json`:**
    Create a JSON file named `test_email.json` in the same directory as `send_emails.py`. It should have the following structure:
    ```json
    [
      {
        "university": "Trinity College Dublin",
        "emails": [
          "email1@example.com",
          "email2@example.com"
        ],
        "total_emails_found": 2
      },
      {
        "university": "Another University",
        "emails": [
          "contact@anotheruni.edu"
        ],
        "total_emails_found": 1
      }
    ]
    ```
    The script will iterate through each `university` entry and send emails to all addresses in its `emails` list.

4.  **Create `.env` for Credentials:**
    Create a file named `.env` in the same directory as `send_emails.py`. **This file is crucial for security and will NOT be uploaded to GitHub.**
    Add your email credentials and SMTP server details here:
    ```
    YOUR_EMAIL="your_sending_email@example.com"
    YOUR_PASSWORD="your_email_app_password" # Use App Password for Gmail with 2FA
    SMTP_SERVER="smtp.gmail.com" # Your email provider's SMTP server (e.g., smtp.office365.com)
    SMTP_PORT=465 # Common ports: 465 for SSL, 587 for TLS
    ```
    * **For Gmail users:** If you have 2-Factor Authentication (2FA) enabled, you *must* generate an "App password" instead of using your regular Gmail password. You can do this in your Google Account security settings.

5.  **Customise `email_template.html`:**
    Open `email_template.html` and ensure it contains the placeholder `{{Recipient Department/Office}}` where you want the university/office name to appear (e.g., `Dear TCD,`). Also, ensure `{{Your Name/Project Name}}` and `{{Your Affiliation/Study Area}}` are used for your sign off.
    Remember to update any links (e.g., survey, privacy policy) to your actual URLs.

6.  **Run the Script:**
    ```bash
    python send_emails.py
    ```
    The script will send emails and print status messages to your console.

### Recommended: Using a Virtual Environment

For better dependency management and to avoid conflicts with other Python projects, it's highly recommended to use a virtual environment:

1.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    ```
2.  **Activate Virtual Environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
3.  Then, proceed with `pip install -r requirements.txt`. Remember to activate the environment each time you work on the project.