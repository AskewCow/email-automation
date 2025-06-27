## Version 1

This initial version was used for sending around 60 emails to different contacts within our own college, with small personalisations in each email.

This version uses:
* **Excel File**: For contact addresses and names (`email-list.xlsx`). It expects columns like "Title", "First Name", and "Email".
* **HTML File**: For the email template (`email_template.html`). It uses placeholders like `{{title}}`, `{{first_name}}`, and `{{sender_name}}`.

### Files in this Version

* `send_emails.py`: The core Python script that handles reading the Excel file, populating the HTML template, and sending emails.
* `email_template.html`: The HTML template for your email.
* `requirements.txt`: Lists the Python dependencies (`pandas`, `openpyxl`, `python-dotenv`).
* `.env`: (You will need to create this) Stores your sensitive email credentials. **This file is excluded from GitHub.**
* `email-list.xlsx`: (You will create/provide this) Your Excel file containing recipient data. **This file should be excluded from GitHub if it contains sensitive data. The one present is simply for illustration purposes.**

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

3.  **Prepare `email-list.xlsx`:**
    Create an Excel file named `email-list.xlsx` in the same directory as `send_emails.py`. It should have at least the following columns:
    * `Title` (e.g., "Prof.", "Dr.")
    * `First Name` (e.g., "John", "Jane")
    * `Email` (e.g., "john.doe@example.com")
    The script will read these columns to personalise your emails.

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
    Open `email_template.html` and ensure it contains the placeholders `{{title}}`, `{{first_name}}`, and `{{sender_name}}` where you want the personalised information to appear.
    For example:
    ```html
    <p>Dear {{title}} {{first_name}},</p>
    <p>Sincerely,<br />
        {{sender_name}}<br />
        Business &amp; Computer Science</p>
    ```
    Also, remember to update any links (e.g., survey, privacy policy) to your actual URLs.

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