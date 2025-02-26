import logging
import firebase_admin
from firebase_admin import credentials, firestore
from config import GOOGLE_APPLICATION_CREDENTIALS,FIRESTORE_COLLECTION

logging.basicConfig(level=logging.DEBUG)

# # Load credentials
# cred = credentials.Certificate(GOOGLE_APPLICATION_CREDENTIALS)
# firebase_admin.initialize_app(cred)

# Connect to Firestore
try:
    db = firestore.Client(FIRESTORE_COLLECTION)
    logging.info("✅ Firestore connection successful!")
except Exception as e:
    logging.error(f"❌ Firestore connection failed: {e}")

servers_collection = db.collection(FIRESTORE_COLLECTION)

def set_default_twitch_channel(guild_id: int, channel_id: str):
    """Set the default Twitch channel for a server in Firestore."""
    servers_collection.document(str(guild_id)).set({"twitch_channel_id": channel_id})
    print(f"✅ Set default Twitch channel for {guild_id}: {channel_id}")

def get_default_twitch_channel(guild_id: int) -> str:
    """Retrieve the default Twitch channel ID for a server from Firestore."""
    doc = servers_collection.document(str(guild_id)).get()
    if doc.exists:
        return doc.to_dict().get("twitch_channel_id")
    return None  # No default set

def set_schedule_message(guild_id: int, schedule_message: str):
    """Set the schedule message for a server in Firestore."""
    servers_collection.document(str(guild_id)).set({"schedule_message": schedule_message})
    print(f"✅ Set default Twitch channel for {guild_id}: {schedule_message}")

def get_schedule_message(guild_id: int) -> str:
    """Retrieve the schedule message for a server from Firestore."""
    doc = servers_collection.document(str(guild_id)).get()
    if doc.exists:
        return doc.to_dict().get("schedule_message")
    return None  # No default set