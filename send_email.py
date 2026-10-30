import json
import os
import smtplib
from email.message import EmailMessage

with open("testreport.json", "r") as file:
    report = json.load(file)

gmail = os.environ["GMAIL_ADDRESS"]
password = os.environ["GMAIL_APP_PASSWORD"]
recipient = os.environ["EMAIL_TO"]

status = report["overall_status"].upper()

msg = EmailMessage()
msg["Subject"] = f"[DevOps CI] {status}: {report['repository_name']}"
msg["From"] = gmail
msg["To"] = recipient

msg.set_content(
    f"""DevOps Test Report

Repository: {report['repository_name']}
Branch: {report['branch']}
Commit: {report['commit_sha']}
Pipeline ID: {report['pipeline_run_id']}

Total tests: {report['total_tests']}
Passed: {report['passed']}
Failed: {report['failed']}
Skipped: {report['skipped']}

Overall Status: {status}
"""
)

with open("testreport.json", "rb") as file:
    msg.add_attachment(
        file.read(),
        maintype="application",
        subtype="json",
        filename="testreport.json"
    )

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(gmail, password)
    server.send_message(msg)

print(f"Email report sent successfully to {recipient}")
