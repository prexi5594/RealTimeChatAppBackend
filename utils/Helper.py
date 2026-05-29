from flask_mail import Message
from threading import Thread


def validate_fields(data, fields):

    for field in fields:

        if field not in data:
            return False

        if not data[field]:
            return False

    return True


def format_timestamp(timestamp):
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    return formatted_time

def send_async_email(app, mail, msg):

    with app.app_context():

        try:
            mail.send(msg)

            print("EMAIL SENT SUCCESSFULLY")

        except Exception as e:

            print("EMAIL FAILED:", str(e))


def send_otp_email(app, mail, email, otp):

    msg = Message(
        subject="QuickChat OTP Code",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = f"""
Your QuickChat OTP Code is:

{otp}

This code expires soon.
"""

    Thread(
        target=send_async_email,
        args=(app, mail, msg)
    ).start()