from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SlackMessage:
    author: str
    text: str
    timestamp: str
    permalink: str


@dataclass
class SlackThread:
    channel: str
    thread_id: str
    messages: List[SlackMessage]
    raw_metadata: Dict
    