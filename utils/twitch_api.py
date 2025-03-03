from config import TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.type import TwitchResourceNotFound
from utils.helpers import timestamp_discord

async def get_twitch_schedule(channel_id,schedule_limit):
    """Get the schedule of a twitch channel in discord timestamp format"""
    # initialize the twitch instance
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    
    # get the channel's stream schedule
    try:
        response = await twitch.get_channel_stream_schedule(channel_id)
    except TwitchResourceNotFound:
        return None
    
    # iterate through the schedule and return the first `schedule_limit` entries that are not canceled
    schedule_count = 0
    schedule_return = []
    async for segment in response:
        if segment.canceled_until is not None:
            continue
        schedule_return.append(timestamp_discord(segment.start_time))
        schedule_count += 1
        if schedule_count == schedule_limit:
            break
    
    # close the twitch instance
    await twitch.close()

    return "\n".join(schedule_return)

async def get_twitch_user_id(channel):
    """Get the user id and display name of a twitch channel"""
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    user = await first(twitch.get_users(logins=channel))
    await twitch.close()
    return user.id, user.display_name