import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
OLLAMA_URL = os.environ.get("OLLAMA_URL")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
OLLAMA_CHAT_URL = os.environ.get("OLLAMA_CHAT_URL")
LLM_MODEL = os.environ.get("LLM_MODEL")