import os
from flask import Flask, json
from skpy import Skype, SkypeEventLoop, SkypeNewMessageEvent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger
from datetime import datetime, timedelta

app = Flask(__name__)

username = "input_username_or_email_here"
password = "input_password_here"

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data", "time.json")
time_data = json.load(open(json_url))
print(time_data)

sk = Skype(username, password) # connect to Skype

user = sk.user # you
contacts = sk.contacts # your contacts
chats = sk.chats # your conversations

def sendMsg():
    """ Function for test purposes. """
    mins = 10
    now = datetime.now() + timedelta(minutes=mins)
    current_time = now.strftime("%H:%M")
    if current_time == time_data["johr"] or current_time == time_data["asr"] or current_time == time_data["maghrib"]:
        print("sending message")
        prayer = ""
        if current_time == time_data["johr"]:
            prayer = "Johr"
        elif current_time == time_data["asr"]:
            prayer = "Asr"
        elif current_time == time_data["maghrib"]:
            prayer = "Maghrib"
        ch = chats["19:group_id@thread.skype"]  # add the group_id of skype, inspect the network data in web.skype.com
        msg = ch.sendMsg("<at id=\"*\">all</at> Reminder: " + prayer + " Salat in " + str(mins) + " minutes.", rich=True)
    print(f"Scheduler is alive! {current_time}")


sched = BackgroundScheduler(daemon=True)
cron1 = CronTrigger(day_of_week='mon-fri', hour='11-20', minute='*/5', timezone='Asia/Dhaka')
trigger = OrTrigger([cron1])
sched.add_job(sendMsg, trigger)
sched.start()
    
# Auto reply system.
# class SkypePing(SkypeEventLoop):
#     def __init__(self):
#         super(SkypePing, self).__init__(username, password)
#         print("initialized! watching for events")
#     def onEvent(self, event):
#         if isinstance(event, SkypeNewMessageEvent) and not event.msg.userId == self.userId :
#             # sending automated reply
#             event.msg.chat.sendMsg("Hi! Aqeeb is currently not available. If urgent you can call him at 91********")

# skyp = SkypePing()
# skyp.loop()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
