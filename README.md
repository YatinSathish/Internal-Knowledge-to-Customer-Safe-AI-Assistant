# Internal-Knowledge-to-Customer-Safe-AI-Assistant

This is an RAG system that does the following:
- Ingests internal Slack conversations.
- Classifies them using AI to find source of truth and customer safe data.

## Architecture Overview
![System Architecture Diagram](assets/architecture.png)

## Setup:
- Create a `.env` in the root directory and enter your google api key (`GEMINI_API_KEY=<your api key>`).
- [Create a virtual environment if needed.](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
- Install the required dependencies from the `requirements.txt` file: `pip install -r requirements.txt`
- The project uses a central controller `main.py` to manage all of the tasks.
    - **Initial Setup (Ingest & Index):** `python main.py --setup`
    - **Start the REST API:** `python main.py --api`
    - **Query (Internal):** `python main.py --query "What is the API rate limit?"`
    - **Query (Customer Mode):** `python main.py --query "What is the API rate limit?" --customer`