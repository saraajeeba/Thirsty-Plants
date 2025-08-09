import cv2
import time
import smtplib
from email.mime.text import MIMEText
import os
import json

rain_status = False
last_alert_sent = False

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ config.json not found!")
        return None

def send_email_alert(to_email, message):
    config = load_config()
    if not config:
        return

    smtp_server = config["smtp_server"]
    smtp_port = config["smtp_port"]
    sender_email = config["sender_email"]
    sender_password = config["sender_password"]

    try:
        msg = MIMEText(message)
        msg["Subject"] = "Rain Alert!"
        msg["From"] = sender_email
        msg["To"] = to_email

        if smtp_port == 465:  # SSL
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:  # STARTTLS
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def detect_rain():
    global rain_status, last_alert_sent
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera not found or cannot be opened.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        count = cv2.countNonZero(edges)

        print("Edge count:", count)

        if count > 15000:
            rain_status = True
            status_text = "Raining"

            if not last_alert_sent and os.path.exists("user_email.txt"):
                with open("user_email.txt", "r") as ef:
                    email = ef.read().strip()
                if email:
                    send_email_alert(email, "It is raining! Please take precautions.")
                    last_alert_sent = True
        else:
            rain_status = False
            status_text = "Not Raining"
            last_alert_sent = False

        with open("rain_status.txt", "w") as f:
            f.write(status_text)

        display_frame = frame.copy()
        cv2.putText(display_frame, status_text, (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255) if rain_status else (0, 255, 0), 2)
        cv2.imshow("Camera View", display_frame)
        cv2.imshow("Edges", edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(5)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_rain()
