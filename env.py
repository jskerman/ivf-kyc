import os
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")