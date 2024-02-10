from datetime import datetime, timedelta

# Parse Newgrounds-style date/time string
def parse_time(date_string, time_string):
    datetime_string = f"{date_string} {time_string[:-4]}"

    date_object = datetime.strptime(datetime_string, "%b %d, %Y %I:%M %p")
    # All Newgrounds times are in EST, convert to UTC
    return date_object - timedelta(hours=5)

# Parse human-readable duration ("x min x sec") into seconds
def parse_duration(duration):
    duration = duration.split()

    minutes = int(duration[0])
    seconds = int(duration[2])

    return minutes * 60 + seconds
