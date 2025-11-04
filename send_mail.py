import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- Environment Variables ---
sender_email = os.getenv("SENDER_EMAIL")
password = os.getenv("GMAIL_APP_PASSWORD")

resume_path = "MOHAN_A_AWS_DevOps_Engineer_Resume.pdf"
json_path = "mails.json"

# --- Load HR data ---
with open(json_path, "r", encoding="utf-8") as f:
    hr_list = json.load(f)

for hr in hr_list:
    hr_name = hr.get("name", "")
    hr_email = hr.get("email", "")
    company_name = hr.get("company", "")
    subject = hr.get("subject", "").format(company_name=company_name)
    summary = hr.get("summary", "").format(company_name=company_name)

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

    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = hr_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    # Attach resume
    with open(resume_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={resume_path.split('/')[-1]}")
    msg.attach(part)

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)

    print(f"✅ Sent mail to {hr_name} ({hr_email}) at {company_name}")
