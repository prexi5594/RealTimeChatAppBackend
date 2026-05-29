from flask_mail import Message
import threading


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

def send_otp_email(mail, email, otp, app):

    def send_async(app_instance):
        try:
            with app_instance.app_context():   

                msg = Message(
                    "QuickChat OTP Code",
                    sender=app_instance.config["MAIL_USERNAME"],
                    recipients=[email]
                )

                msg.body = f"Your OTP is: {otp}"
                mail.send(msg)

                print("OTP email sent successfully")

        except Exception as e:
            print(f"MAIL ERROR: {str(e)}")

    threading.Thread(
        target=send_async,
        args=(app,)
    ).start()