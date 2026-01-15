import json
from datamodels import SlackThread, SlackMessage
import os 

def ingest(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    threads = []
    for channel in data.get('channels', []):
        channel_name = channel['name']

        for thread in channel.get('threads', []):
            messages = []
            thread_id = thread['id']

            for mesg in thread.get('messages', []):
                messages.append(
                    SlackMessage(
                        author=mesg['author'],
                        text=mesg['text'],
                        timestamp=mesg['timestamp'],
                        permalink=mesg['permalink']
                    )
                )
            
            threads.append(
                SlackThread(
                    channel=channel_name,
                    thread_id=thread['id'],
                    messages=messages,
                    raw_metadata={
                        "source": "slack",
                        "channel": channel_name,
                    }
                )
            )
    return threads
