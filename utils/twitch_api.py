from config import TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import TwitchResourceNotFound
from utils.helpers import timestamp_discord

async def get_twitch_schedule(channel_id,schedule_limit):
    # initialize the twitch instance, this will by default also create a app authentication for you
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    try:
        response = await twitch.get_channel_stream_schedule(channel_id,first=schedule_limit)
    except TwitchResourceNotFound:
        return None
    
    schedule_return = []
    for segment in response.segments:
        schedule_return.append(timestamp_discord(segment.start_time))
    await twitch.close()
    return "\n".join(schedule_return)

async def get_twitch_user_id(channel):
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    user = await first(twitch.get_users(logins=channel))
    await twitch.close()
    return user.id, user.display_name