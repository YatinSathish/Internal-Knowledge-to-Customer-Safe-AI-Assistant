import json
from datamodels import SlackThread, SlackMessage

def ingest(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)