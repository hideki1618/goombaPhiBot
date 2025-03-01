import logging
from firebase_admin import credentials, firestore
from google.cloud.exceptions import NotFound, GoogleCloudError
from config import FIRESTORE_COLLECTION, GOOGLE_APPLICATION_CREDENTIALS

logging.basicConfig(level=logging.DEBUG)

# Connect to Firestore
try:
    db = firestore.Client()
    logging.info("✅ Firestore connection successful!")
except Exception as e:
    logging.error(f"❌ Firestore connection failed: {e}")

servers_collection = db.collection(FIRESTORE_COLLECTION)

def set_default_twitch_channel(guild_id: int, channel_id: str):
    """Set the default Twitch channel for a server in Firestore."""
    server_doc = servers_collection.document(str(guild_id))

    try:
        
        server_doc.update({"twitch_channel_id": channel_id})  # ✅ Prevents overwriting

    except NotFound:
        server_doc.set({"twitch_channel_id": channel_id}, merge=True)
    except GoogleCloudError as e:
        raise GoogleCloudError(f"Error updating database: {e}")

def get_default_twitch_channel(guild_id: int) -> str:
    """Retrieve the default Twitch channel ID for a server from Firestore."""
    doc = servers_collection.document(str(guild_id)).get()
    if doc.exists:
        return doc.to_dict().get("twitch_channel_id")
    return None  # No default set

def set_schedule_message(guild_id: int, schedule_message: str):
    """Set the schedule message for a server in Firestore."""
    server_doc = servers_collection.document(str(guild_id))
    try:
        
        # 🔄 Update only the necessary field
        server_doc.update({"schedule_message": schedule_message})  # ✅ Prevents overwriting
        
    except NotFound:
        server_doc.set({"schedule_message": schedule_message}, merge=True)        
    except GoogleCloudError as e:
        raise GoogleCloudError(f"Error updating database: {e}")

def get_schedule_message(guild_id: int) -> str:
    """Retrieve the schedule message for a server from Firestore."""
    doc = servers_collection.document(str(guild_id)).get()
    if doc.exists:
        return doc.to_dict().get("schedule_message")
    return None  # No default set