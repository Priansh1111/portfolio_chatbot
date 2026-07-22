import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
OLLAMA_URL = os.environ.get("OLLAMA_URL")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")