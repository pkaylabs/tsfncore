import array

import requests

from core import settings


def send_sms(message: str, recipients: array.array, sender: str = settings.SENDER_ID):
    '''Sends an SMS to the specified recipients'''
    print("KEYS")
    print(settings.ARKESEL_API_KEY)
    print(settings.SENDER_ID)
    
    header = {"api-key": settings.ARKESEL_API_KEY, 'Content-Type': 'application/json',
              'Accept': 'application/json'}
    SEND_SMS_URL = "https://sms.arkesel.com/api/v2/sms/send"
    payload = {
        "sender": sender,
        "message": message,
        "recipients": recipients
    } 
    try:
        response = requests.post(SEND_SMS_URL, headers=header, json=payload)
    except Exception as e:
        print(f"Error: {e}")
        return False
    else:
        print(response.json())
        return response.json()