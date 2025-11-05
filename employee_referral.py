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
json_path = "employee_referral.json"
log_path = "sent_employee_log.txt"

# --- Load Employee Data ---
try:
    with open(json_path, "r", encoding="utf-8") as f:
        employee_list = json.load(f)
except Exception as e:
    raise RuntimeError(f"❌ Failed to read {json_path}: {e}")

# --- Initialize Log File ---
with open(log_path, "a", encoding="utf-8") as log_file:
    log_file.write(f"\n\n=== Employee Mail Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")

# --- SMTP Loop ---
for emp in employee_list:
    emp_name = emp.get("name", "Employee")
    emp_email = emp.get("email", "")
    company_name = emp.get("company", "")

    if not emp_email:
        print(f"⚠️ Skipping {emp_name} (no email found)")
        continue

    subject = f"Request for Referral – DevOps Engineer Role at {company_name}"

    # --- Email Body (Second Option) ---
    html_body = f"""
    <html>
    <body>
    <p>Hi {emp_name},</p>

    <p>Hope you’re doing well. I noticed an opening for a <b>DevOps Engineer</b> at <b>{company_name}</b> and wanted to check if you’d be open to referring me for the role.</p>

    <p>I have <b>4.8 years of experience</b> in DevOps, including <b>AWS, Docker, Kubernetes, Terraform, Jenkins</b>, and <b>CI/CD pipeline automation</b>.</p>

    <p>Please let me know if you’d be comfortable referring me; I’ve attached my resume for your review.</p>

    <p>Thanks a lot for your time and help!</p>

    <p>Best regards,<br>
    <b>A. Mohan</b><br>
    AWS & DevOps Engineer<br>
    📞 +91 9121844231<br>
    ✉️ <a href="mailto:{sender_email}">{sender_email}</a><br>
    🔗 <a href="https://www.linkedin.com/in/mohan-a-8a0011397">LinkedIn Profile</a>
    </p>
    </body>
    </html>
    """

    # --- MIME Message ---
    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = emp_email
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
        print(f"✅ Sent mail to {emp_name} ({emp_email}) at {company_name}")

        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"✅ {datetime.now().strftime('%H:%M:%S')} - Sent to {emp_name} ({emp_email}) at {company_name}\n")

    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Check Gmail App Password and 2FA.")
        break
    except Exception as e:
        print(f"❌ Failed to send email to {emp_email}: {e}")
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"❌ Failed to send mail to {emp_email}: {e}\n")
