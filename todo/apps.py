from django.apps import AppConfig
import threading
import time
import requests
import sys
from django.conf import settings
from datetime import datetime, timedelta


# python manage.py runserver --noreload

def send_mail(mail, subject, text):
    if mail == "" or "@gmail.com" not in mail or subject == "" or text == "":
        raise ValueError()
    api_key = settings.API_KEY
    domain = settings.DOMAIN
    from_address = settings.FROM
    api_key = api_key
    domain = domain
    s = f"https://api.mailgun.net/v3/{domain}/messages"
    print("sending...")
    return requests.post(s,
        auth=("api", api_key),
        data={
            "from": from_address,
            "to": [mail],
            "subject": subject,
            "text": text
            })

def hourly_task():
    time.sleep(2)
    print("Running hourly task....")
    from todo.models import ListItem
    while True:
        current_date = datetime.now().date()
        listItems = ListItem.objects.all()
        for item in listItems:
            if current_date == (item.due_date - timedelta(days=1)):
                subject = f"TODO List, Item is due: {item.item_name}"
                text = f"Item details: Text: {item.item_text}, Status: {item.status}, Due Date: {item.due_date}"
                email = None
                # send_mail(email, subject, text)
        time.sleep(3600)

class TodoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'todo'
    thread_started = False
    def ready(self):
        if 'test' not in sys.argv:
            if not TodoConfig.thread_started:
                TodoConfig.thread_started = True
                thread = threading.Thread(target=hourly_task)
                thread.daemon = True
                thread.start()