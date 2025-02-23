def timestamp_discord(info_date):
    time_iso = int(info_date.timestamp())
    return f"<t:{time_iso}:F>"