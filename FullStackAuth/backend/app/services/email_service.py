
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL")


def _send_email(message: EmailMessage) -> None:
    """Validate SMTP settings and send an email."""

    required_settings = {
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USERNAME": SMTP_USERNAME,
        "SMTP_PASSWORD": SMTP_PASSWORD,
        "SMTP_FROM_EMAIL": SMTP_FROM_EMAIL,
    }

    missing = [
        name
        for name, value in required_settings.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            f"Missing email configuration: {', '.join(missing)}"
        )

    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT,
        timeout=15,
    ) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(message)


def send_password_reset_otp(
    recipient_email: str,
    otp: str,
) -> None:
    """Send a password-reset OTP to the registered email."""

    message = EmailMessage()
    message["Subject"] = "FullStackAuth - Password Reset OTP"
    message["From"] = SMTP_FROM_EMAIL or ""
    message["To"] = recipient_email

    message.set_content(
        f"""Hello,

We received a request to reset your FullStackAuth password.

Your verification code is: {otp}

This code expires in 5 minutes. If you did not request this,
you can ignore this email.

For your security, do not share this code with anyone.

FullStackAuth Team
"""
    )

    _send_email(message)


def send_registration_email(
    recipient_email: str,
    username: str,
) -> None:
    """Send a welcome email after successful registration."""

    message = EmailMessage()
    message["Subject"] = "FullStackAuth - Registration Successful"
    message["From"] = SMTP_FROM_EMAIL or ""
    message["To"] = recipient_email

    message.set_content(
        f"""Hello {username},

Welcome to FullStackAuth!

Your account has been created successfully.

You can now log in using your registered credentials.

If you did not create this account, please contact support.

Regards,
FullStackAuth Team
"""
    )

    _send_email(message)


def send_login_notification(
    recipient_email: str,
    username: str,
    login_time: str,
) -> None:
    """Notify the user after a successful login."""

    message = EmailMessage()
    message["Subject"] = "FullStackAuth - New Login Notification"
    message["From"] = SMTP_FROM_EMAIL or ""
    message["To"] = recipient_email

    message.set_content(
        f"""Hello {username},

A successful login to your FullStackAuth account occurred.

Login time (UTC): {login_time}

If this was you, no action is needed.

If you do not recognize this login, change your password
and contact support.

Regards,
FullStackAuth Team
"""
    )

    _send_email(message)
