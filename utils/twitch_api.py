from config import TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from utils.helpers import timestamp_discord

async def get_twitch_schedule(channel,schedule_limit):
    # initialize the twitch instance, this will by default also create a app authentication for you
    twitch = await Twitch(TWITCH_CLIENT_ID, TWITCH_ACCESS_TOKEN)
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins=channel))
    schedule = await twitch.get_channel_stream_schedule(user.id)
    schedule_count = 0
    schedule_return = []
    async for segment in schedule:
        schedule_return.append(timestamp_discord(segment.start_time))
        schedule_count += 1
        if schedule_count == schedule_limit:
            break
    await twitch.close()
    return "\n".join(schedule_return)