# 📧 Bulk Email Campaign Sender (Streamlit App)

This is a Python-based web application built with **Streamlit** designed to help users send personalized bulk email campaigns directly from their own Gmail account. It is ideal for small businesses, marketing teams, or individuals who need to send customized emails to a list of recipients without relying on complex, expensive email service platforms.

## ✨ Features

  * **Custom Sender:** Send emails directly from a specified Gmail address using a secure App Password.
  * **Bulk Sending:** Reads recipient emails from a user-uploaded Excel file (`.xlsx`).
  * **Personalization:** Supports dynamic content fields (e.g., `{name}`) in the email body, which are populated from the contacts file.
  * **Attachments:** Supports uploading multiple files to be included as attachments in every email.
  * **Real-time Status:** Provides live feedback on login attempts, successful sends, and failures using Streamlit's `st.status` container.
  * **Security Reminder:** Prompts users to use a secure **Gmail App Password** instead of their main account password.

-----

## 🚀 How to Use the App

To run a campaign, you need four things: a contacts file, your Gmail credentials, the email content, and a stable internet connection.


### 1\. Prepare Your Data

**Contacts File** Must be an **Excel file (`.xlsx`)** and contain a column strictly named **`Email`**. You can optionally include a **`Name`** column for personalization.
**Gmail App Password** This app uses the SMTP protocol. You **must** enable **2-Factor Authentication (2FA)** on your Gmail account and generate a dedicated **App Password** to use for the app password field. Standard Gmail passwords will be rejected by Google for security reasons.

### 2\. Run the Campaign
use this link to launch the program https://bulkmails.streamlit.app/
1.  **Enter Credentials:** Provide your **Sender Gmail Address** and the **Gmail App Password**.
2.  **Upload Files:** Upload your **Contacts File** (`.xlsx`) and any **Attachments**.
3.  **Define Content:** Fill in the **Subject**, **Body** (use `{name}` for personalization), and **Signature**.
4.  **Start:** Click the **"🚀 Start Sending Emails"** button. The app will open a progress tracker and begin sending emails one by one.

-----

## ⚙️ Local Setup (For Developers)

If you want to run this application on your local machine:

### Prerequisites

You need **Python 3.8+** installed on your system. Using a **Virtual Environment** is highly recommended.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Adewuyipraise/bulk-email-app.git
    cd bulk-email-app
    ```
2.  **Install Dependencies:** The required libraries are listed in the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

### Execution

Run the Streamlit app from your terminal:

```bash
streamlit run appstreamlit.py
```

-----

## 🌐 Deployment

This application is designed for easy deployment on **Streamlit Community Cloud** (which is how this version is likely being hosted\!). The platform automatically uses the `requirements.txt` file to set up the environment.

  * **Repository:** `https://github.com/Adewuyipraise/bulk-email-app`
  * **Main File:** `appstreamlit.py`

-----

## ⚠️ Disclaimer

This tool is intended for responsible use, primarily for sending legitimate communications to users who have opted in. Please be aware of the daily sending limits and policies of your email provider (like Gmail) to avoid account suspension or being flagged as spam. The developer is not responsible for misuse of this application.
