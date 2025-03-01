from config import TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from utils.helpers import timestamp_discord

async def get_twitch_schedule(channel_id,schedule_limit):
    # initialize the twitch instance, this will by default also create a app authentication for you
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    response = await twitch.get_channel_stream_schedule(channel_id)

    if not response or "data" not in response or not response["data"]:
        return None  # No schedule found
    
    schedule_count = 0
    schedule_return = []
    async for segment in response:
        schedule_return.append(timestamp_discord(segment.start_time))
        schedule_count += 1
        if schedule_count == schedule_limit:
            break
    await twitch.close()
    return "\n".join(schedule_return)

async def get_twitch_user_id(channel):
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    user = await first(twitch.get_users(logins=channel))
    await twitch.close()
    return user.id, user.display_name