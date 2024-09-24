import django.dispatch
from django.dispatch import receiver
import requests
import os

# Define the signal
makemigrations_signal = django.dispatch.Signal()

@receiver(makemigrations_signal)
def send_to_slack(sender, output, **kwargs):
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    payload = {'text': output}
    
    response = requests.post(slack_webhook_url, json=payload)

    if response.status_code != 200:
        print(f"Failed to send message to Slack: {response.status_code}, {response.text}")