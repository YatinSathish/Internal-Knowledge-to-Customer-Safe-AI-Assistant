from datamodels import SlackThread, Chunk
from ingestion import ingest

def chunk_threads(threads):
    chunks = []

    for thread in threads:
        combined_text = []
        permalinks = []

        for msg in thread.messages:
            combined_text.append(f"{msg.author}: {msg.text}")
            permalinks.append(msg.permalink)

        chunk_text = "\n".join(combined_text)
        # print(chunk_text)
        chunk = Chunk(
            chunk_id=f"{thread.channel}-{thread.thread_id}",
            text=chunk_text,
            thread_id=thread.thread_id,
            channel=thread.channel,
            message_permalinks=permalinks,
            metadata={
                "source": "slack",
                "channel": thread.channel,
            },
        )

        chunks.append(chunk)

    return chunks

threads = ingest("data/mock_slack.json")
chunks = chunk_threads(threads)
print(chunks[0])
