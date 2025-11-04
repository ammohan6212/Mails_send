import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- Configuration ---
sender_email = "mohanagasta1998@gmail.com"
password = "bofjpfgnlezmqexu"  # Use Gmail App Password
resume_path = "MOHAN_A_AWS_DevOps_Engineer_Resume.pdf"
json_path = "mails.json"  # Path to JSON file containing HR details

# --- Read JSON data ---
with open(json_path, "r", encoding="utf-8") as f:
    hr_list = json.load(f)

# --- Loop through HR list ---
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
    ✉️ <a href="mailto:mohanagasta1998@gmail.com">mohanagasta1998@gmail.com</a><br>
    🔗 <a href="https://www.linkedin.com/in/mohan-a-8a0011397">LinkedIn Profile</a>
    </p>
    </body>
    </html>
    """

    # --- Create the email message ---
    msg = MIMEMultipart("mixed")
    msg["From"] = sender_email
    msg["To"] = hr_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    # --- Attach resume ---
    try:
        with open(resume_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={resume_path.split('/')[-1]}")
        msg.attach(part)
    except FileNotFoundError:
        print(f"⚠️ Resume file not found: {resume_path}")
        continue

    # --- Send the email ---
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        print(f"✅ Email sent successfully to {hr_name} ({hr_email}) at {company_name}")
    except Exception as e:
        print(f"❌ Failed to send email to {hr_name} ({hr_email}): {e}")

print("\n🎉 All emails processed successfully!")
