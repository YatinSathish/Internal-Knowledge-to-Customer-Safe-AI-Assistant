from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional

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
    # output derived from classifier
    knowledge_worthy: Optional[bool] = None
    source_of_truth: Optional[bool] = None
    customer_safe: Optional[bool] = None
    classification_reason: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(d):
        return Chunk(**d)