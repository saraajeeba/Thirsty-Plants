import smtplib
from email.mime.text import MIMEText

# ==== CHANGE THESE BEFORE RUNNING ====
sender_email = "saralizzie6@gmail.com"        # Gmail address you created the App Password for
sender_password = "rhxdniwbirxqphcp"        # Your 16-char App Password (no spaces)
receiver_email = "princesswonder08@gmail.com.com"          # Where to send the test email
# ======================================

# Create the email
msg = MIMEText("This is a test email from Python using Gmail App Password.")
msg["Subject"] = "Test Email"
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    print("Connecting to Gmail SMTP...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        print("Logging in...")
        server.login(sender_email, sender_password)
        print("Sending email...")
        server.send_message(msg)
    print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)
