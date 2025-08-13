from plyer import notification
from datetime import datetime


import os
import requests

from dotenv import load_dotenv


def send_warnings(title,file_path):
    '''this function will send a desktop notification when ever the files are changed'''

    if not isinstance(title, str) or not title.strip():
            print("Invalid data type...")
            return

    # Create message for a single file
    message = f"File change detected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n- {file_path}"

    try:
        notification.notify(
            title = title,
            message =message,
            timeout = 5 #seconds
        )
    except Exception as e:
        print(f"Notification Failed:{e}")

load_dotenv()

DISCORD_WEBHOOK_URL=os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alerts(message):
    if not DISCORD_WEBHOOK_URL:
          print("No discord webhook url found..")
          return False
    payload = {"content":message}
     
    try:
          responce =requests.post(DISCORD_WEBHOOK_URL,json=payload)
          if responce.status_code==204:
               print("Alert send to discord..")
               return True
          else:
               print("Failed to send alert..")
               return False
    except Exception as e:
        print("Error sending alert:{e}")
        return False

