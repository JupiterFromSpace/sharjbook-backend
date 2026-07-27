from accounts.tasks import send_otp_email

def send_otp(email, code):
    send_otp_email.delay(email, code)
    