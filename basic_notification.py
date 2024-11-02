import datetime
import time


tasks = [
    {"task_name": "Finish project report", "due_date": datetime.datetime(2024, 11, 2, 15, 0), "reminder_intervals": [60, 30, 10]},  # in minutes
    {"task_name": "Team meeting", "due_date": datetime.datetime(2024, 11, 2, 17, 0), "reminder_intervals": [60, 30, 10]},
    {"task_name": "Code review", "due_date": datetime.datetime(2024, 11, 3, 12, 0), "reminder_intervals": [120, 60, 15]},
]


sent_notifications = {}

def send_notification(task_name, minutes_left):
    print(f"🔔 Reminder: '{task_name}' is due in {minutes_left} minutes!")

def check_notifications():
    current_time = datetime.datetime.now()
    for task in tasks:
        task_name = task["task_name"]
        due_date = task["due_date"]
        reminder_intervals = task["reminder_intervals"]
        
        time_until_due = (due_date - current_time).total_seconds() / 60  # time in minutes
        
        
        for interval in reminder_intervals:
            if interval >= time_until_due > 0:
                
                reminder_key = f"{task_name}_{interval}_minutes"
                
                
                if reminder_key not in sent_notifications:
                    send_notification(task_name, int(time_until_due))
                    sent_notifications[reminder_key] = True  

if __name__ == "__main__":
    print("Starting notification system...")
    try:
        while True:
            check_notifications()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Notification system stopped.")
