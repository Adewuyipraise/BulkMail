import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
import io
import mimetypes 

#--- Adsense Configuration ---
def display_adsense_ad():
    """Renders the Google AdSense code."""
    # --------------------------------------------------------------------------------
    # IMPORTANT: Replace the placeholders below with your ACTUAL AdSense code.
    # --------------------------------------------------------------------------------

    # The entire ad loading HTML, including the <script> tags.
    # The 'google-js' is for the auto ads script, and the 'ad-unit-js' is for the specific ad block.
    adsense_html = """
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6828896848803720"
     crossorigin="anonymous"></script>
<!-- Bulk Mail -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-6828896848803720"
     data-ad-slot="8587949026"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
    """
    
    # Render the HTML component
    components.html(
        adsense_html, 
        height=150, # Adjust height based on the expected size of the ad
        scrolling=False
    )

# --- Configuration ---
# SMTP Details (Note: SENDER_EMAIL is now dynamic)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# --- Core Email Logic ---
# SENDER_EMAIL parameter added to the function signature
def send_emails(df_contacts, sender_email, app_password, subject, body, signature, attachments_list):
    """
    Connects to SMTP and sends emails with optional multiple attachments.
    Yields status updates for Streamlit's st.status container.
    """
    
    if df_contacts.empty or 'Email' not in df_contacts.columns:
        yield f"Error: Contacts file must contain an 'Email' column.", 'error'
        return 0, 0, []
        
    log = []
    
    # 1. Start SMTP session and login
    try:
        # Use the dynamic sender_email for login
        yield f"Attempting to log in as {sender_email}...", 'info'
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, app_password)
        yield "Login successful. Starting campaign...", 'info'
    except Exception as e:
        yield f"Error logging in to SMTP. Check Sender Email/App Password. Error: {e}", 'error'
        return 0, 0, []

    # Construct the full body template with signature
    body_template = body + "\n\n---\n" + signature
    
    sent_count = 0
    fail_count = 0

    # 2. Iterate through contacts and send
    for index, row in df_contacts.iterrows():
        recipient = row.get('Email', 'N/A')
        name = row.get('Name', 'Customer')
        
        # Prepare Content
        full_body_plain = body_template.replace('{name}', name) 
        full_body_html = full_body_plain.replace('\n', '<br>')
        
        # Create Main Container
        msg = MIMEMultipart('mixed') 
        msg['From'] = sender_email # Use dynamic sender_email here
        msg['To'] = recipient
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)

        # Create Body Container (Alternative)
        msg_alternative = MIMEMultipart('alternative')
        
        # Check if signature contains HTML (e.g., <img> tag) and force HTML if so.
        if '<img' in full_body_html:
             msg_alternative.attach(MIMEText(full_body_plain, 'plain'))
             msg_alternative.attach(MIMEText(full_body_html, 'html'))
        else:
            msg_alternative.attach(MIMEText(full_body_plain, 'plain'))
            
        msg.attach(msg_alternative)

        # Attachments
        for attachment_filename, attachment_data in attachments_list:
            try:
                # Use mimetypes to correctly guess maintype and subtype
                ctype, encoding = mimetypes.guess_type(attachment_filename)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                
                maintype, subtype = ctype.split('/', 1)

                part = MIMEBase(maintype, subtype)
                part.set_payload(attachment_data)
                encoders.encode_base64(part)
                
                part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
                msg.attach(part) 
            except Exception as e:
                log.append({'email': recipient, 'status': 'Attachment Error'})
                yield f"Warning: Could not attach file {attachment_filename} for {recipient}: {e}", 'warning'

        # Send the email
        try:
            server.sendmail(sender_email, recipient, msg.as_string()) # Use dynamic sender_email here
            sent_count += 1
            log.append({'email': recipient, 'status': 'Sent'})
            yield f"Successfully sent email to {recipient} ({sent_count}/{len(df_contacts)})...", 'success'
        except Exception as e:
            fail_count += 1
            log.append({'email': recipient, 'status': 'Failed'})
            yield f"Failed to send email to {recipient}: {e}", 'error'

    server.quit()
    
    # Final yield to indicate completion
    yield f"Campaign complete! Sent: {sent_count}, Failed: {fail_count}.", 'complete'
    
    return sent_count, fail_count, log

# --- Streamlit UI and Execution ---
def app_ui():
    """Defines the Streamlit application interface."""
    
    st.set_page_config(page_title="Bulk Email Campaign Sender", layout="wide")
    st.title("📧 Bulk Email Campaign Sender")

    st.info("Remember to use a **Gmail App Password** and ensure your account has 2FA enabled and App Passwords set up.")

    # --- AdSense Placement ---
    display_adsense_ad()
    # -------------------------
    
    st.info("Remember to use a **Gmail App Password**...")

    
    # --- 1. Credentials ---
    with st.expander("1. Email Credentials"):
        # NEW INPUT: Sender Email
        sender_email = st.text_input("Sender Gmail Address:", help="The email address you want to send from (e.g., example@gmail.com).")
        
        app_password = st.text_input("Gmail App Password:", type="password", help="Use a secure App Password generated specifically for this application.")

    # --- 2. Uploads ---
    with st.expander("2. Upload Contacts & Attachments"):
        contacts_file = st.file_uploader(
            "Contacts File (Must be a .xlsx with an 'Email' column):", 
            type=['xlsx'], 
            help="Your Excel sheet containing the list of recipients."
        )
        
        attachments_files = st.file_uploader(
            "Optional Files to Attach (Multiple allowed):", 
            type=None, # Allow any file type
            accept_multiple_files=True,
            help="Select one or more files to include as attachments."
        )

    # --- 3. Content ---
    with st.expander("3. Define Email Content", expanded=True):
        subject = st.text_input("Email Subject:", value="Special Offer from Our Business")
        
        st.markdown("**Email Body** (Use `{name}` for personalization):")
        body = st.text_area("Body:", value="Hello {name},\n\nThis is an exclusive business email message just for you. We appreciate your continued support!", height=150)
        
        st.markdown("**Email Signature** (Supports HTML, e.g., `<img src=\"PUBLIC_URL\">` for logo):")
        signature = st.text_area("Signature:", value="Regards,\nYour Company\n[Your Website Link]", height=100)

    # --- 4. Send Button ---
    send_button = st.button("🚀 Start Sending Emails", use_container_width=True)

    if send_button:
        # Input Validation
        if not sender_email or "@" not in sender_email:
            st.error("Please enter a valid Sender Gmail Address.")
            return
        if not app_password:
            st.error("Please enter your Gmail App Password.")
            return
        if not contacts_file:
            st.error("Please upload the contacts file.")
            return

        # 1. Read Contacts File
        try:
            df_contacts = pd.read_excel(contacts_file)
            if 'Email' not in df_contacts.columns:
                 st.error("Contacts file must contain a column named 'Email'.")
                 return
            total_recipients = len(df_contacts)
        except Exception as e:
            st.error(f"Failed to read contacts file: {e}")
            return

        # 2. Process Attachments
        attachments_list = []
        for file in attachments_files:
            attachments_list.append((file.name, file.read()))

        # 3. Start Campaign with Progress Tracker
        st.header("Campaign Progress")
        
        # st.status provides the live progress modal functionality you requested
        with st.status("Initializing campaign...", expanded=True) as status:
            st.write(f"Preparing to send from **{sender_email}** to {total_recipients} recipients...")
            
            progress_log = st.empty()
            log_entries = []
            
            # Start the email sending generator, passing the new sender_email
            email_generator = send_emails(
                df_contacts, 
                sender_email, # <-- New argument passed here
                app_password, 
                subject, 
                body, 
                signature, 
                attachments_list
            )
            
            # Iterate through the generator, updating the UI live
            for update, status_type in email_generator:
                log_entries.append(f"[{status_type.upper()}] {update}")
                
                log_text = "\n".join(log_entries)
                progress_log.code(log_text, language='text')

                if "Login successful" in update:
                    status.update(label=f"Sending {total_recipients} emails...", state="running")
                elif "Campaign complete" in update:
                    status.update(label=update, state="complete", expanded=False)
                elif status_type == 'error':
                    # Keep errors expanded for review
                    status.update(label=update, state="error", expanded=True)
                    # Do not break, allow logging of other successful sends/failures
            
            st.success(f"Campaign sending complete! Please check your sender's 'Sent' folder.")
            
# Run the Streamlit app function
if __name__ == '__main__':
    app_ui()
