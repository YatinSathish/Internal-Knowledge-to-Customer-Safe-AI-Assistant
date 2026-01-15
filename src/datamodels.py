from dataclasses import dataclass, field
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

@dataclass 
class Chunk:
    chunk_id: str
    text: str
    thread_id: str
    channel: str
    message_permalinks: List[str]
    metadata: Dict = field(default_factory=dict)