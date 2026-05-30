import requests
from django.conf import settings

def send_otp(phone, code):
    url = "SMS_IR_ENDPOINT"

    payload = {
        # پارامترهای API
    }

    headers = {
        "X-API-KEY": settings.SMS_IR_API_KEY
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=10
    )

    return response.json()