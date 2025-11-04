import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

# --- Environment Variables ---
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("GMAIL_APP_PASSWORD")

if not sender_email or not password:
    raise EnvironmentError("❌ Missing SENDER_EMAIL or GMAIL_APP_PASSWORD environment variables")

# --- File Paths ---
resume_path = "MOHAN_A_AWS_DevOps_Engineer_Resume.pdf"
json_path = "mails.json"
log_path = "sent_log.txt"

# --- Load HR Data ---
try:
    with open(json_path, "r", encoding="utf-8") as f:
        hr_list = json.load(f)
except Exception as e:
    raise RuntimeError(f"❌ Failed to read {json_path}: {e}")

# --- Initialize Log File ---
with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(f"\n\n=== Mail Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

# --- SMTP Setup ---
for hr in hr_list:
    hr_name = hr.get("name", "HR")
    hr_email = hr.get("email", "")
    company_name = hr.get("company", "")
    subject = hr.get("subject", "").format(company_name=company_name)
    summary = hr.get("summary", "").format(company_name=company_name)

    if not hr_email:
        print(f"⚠️ Skipping {hr_name} (no email found)")
        continue

    # --- Build HTML Body ---
    html_body = f"""
    <html>
    <body>
    <p>Dear {hr_name},</p>
    {summary}
    <p>Please find my resume attached for your review.</p>

    <p>Best regards,<br>
    <b>Mohan A</b><br>
    AWS & DevOps Engineer<br>
    📞 +91 9121844231<br>
    ✉️ <a href="mailto:{sender_email}">{sender_email}</a><br>
    🔗 <a href="https://www.linkedin.com/in/mohan-a-8a0011397">LinkedIn Profile</a>
    </p>
    </body>
    </html>
    """

    # --- Build MIME Message ---
    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = hr_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    # --- Attach Resume ---
    if os.path.exists(resume_path):
        with open(resume_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(resume_path)}")
        msg.attach(part)
    else:
        print(f"⚠️ Resume not found at {resume_path}")

    # --- Send Email ---
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print(f"✅ Sent mail to {hr_name} ({hr_email}) at {company_name}")

        # --- Log Success ---
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"✅ {datetime.now().strftime('%H:%M:%S')} - Sent mail to {hr_name} ({hr_email}) at {company_name}\n")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check your Gmail App Password and 2FA settings.")
        break
    except Exception as e:
        print(f"❌ Failed to send email to {hr_email}: {e}")
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"❌ Failed to send mail to {hr_email}: {e}\n")
