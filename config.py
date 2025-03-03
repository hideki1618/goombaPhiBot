import os
from dotenv import load_dotenv

load_dotenv()
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION")
DISCORD_OWNER_ID = int(os.getenv("DISCORD_OWNER_ID"))
TEST_SERVER_ID = os.getenv("TEST_SERVER_ID")