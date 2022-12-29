import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import time
import schedule
from schedules import schedules
import json
from slack_bolt_app import app as slack_bolt_app


def get_config():
    CONFIG_PATH = "./config.json"
    with open(CONFIG_PATH, 'r') as file:
        config = json.load(file)
        return config

def post_message_alarm(message, slack_client, config):
    channel_name = config["slack"]["channel_name"]
    try:
        response = slack_client.chat_postMessage(channel=channel_name, text=message)
    except SlackApiError as e:
        print(e)

def enroll_schedules(slack_client, config):
    for s in schedules:
        execute_time = s["time"]
        message = s["message"]
        
        schedule.every().day.at(execute_time).do(post_message_alarm, message, slack_client, config)


if __name__ == "__main__":
    load_dotenv()

    # slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
    # config = get_config()
    # enroll_schedules(slack_client, config)

    # a = schedule.get_jobs()
    # print(schedule.get_jobs())
    
    # for s in a:
    #     schedule.cancel_job(s)

    # print(schedule.get_jobs())

    while True:
        schedule.run_pending()
        time.sleep(1)

    SocketModeHandler(slack_bolt_app, os.environ["SLACK_APP_TOKEN"]).start()