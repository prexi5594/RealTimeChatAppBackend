import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import traceback


def validate_fields(data, fields):

    for field in fields:

        if field not in data:
            return False

        if not data[field]:
            return False

    return True


def format_timestamp(timestamp):

    formatted_time = timestamp.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return formatted_time


def send_otp_email(email, otp):
    """
    Send OTP using SendGrid (production safe)
    """

    api_key = os.getenv("SENDGRID_API_KEY")
    sender = os.getenv("MAIL_FROM")

    if not api_key:
        raise Exception("SENDGRID_API_KEY is missing")

    if not sender:
        raise Exception("MAIL_FROM is missing")

    message = Mail(
        from_email=sender,
        to_emails=email,
        subject="QuickChat OTP Verification",
        plain_text_content=f"Your OTP code is: {otp}"
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)

        print("SENDGRID STATUS:", response.status_code)

    except Exception as e:
        print("SENDGRID ERROR:", str(e))
        print(traceback.format_exc())
        raise