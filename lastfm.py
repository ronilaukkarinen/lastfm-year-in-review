import pylast
from datetime import datetime
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Last.fm API
API_KEY = os.getenv('LASTFM_API_KEY')
USERNAME = os.getenv('LASTFM_USERNAME')

# Initialize network without authentication
network = pylast.LastFMNetwork(api_key=API_KEY)

# Set time range for 2024
start_date = int(datetime(2024, 1, 1).timestamp())
end_date = int(datetime(2024, 12, 31, 23, 59, 59).timestamp())

# Get user
user = network.get_user(USERNAME)

# Get all tracks for 2024
all_tracks = []
limit = 900  # Just under the 1000 limit to be safe
current_timestamp = end_date

try:
    print("\nFetching tracks for 2024...")
    print(f"Time range: {datetime.fromtimestamp(start_date)} to {datetime.fromtimestamp(end_date)}")

    while True:
        # Get tracks in batches
        recent_tracks = user.get_recent_tracks(
            limit=limit,
            time_from=start_date,
            time_to=current_timestamp
        )

        batch = list(recent_tracks)
        if not batch:
            break

        all_tracks.extend(batch)
        print(f"Fetched {len(batch)} tracks... (Total so far: {len(all_tracks)})")

        # Update timestamp for next batch
        last_track_timestamp = int(batch[-1].timestamp)
        if last_track_timestamp <= start_date:
            break

        # Set next batch to start just before the last track we got
        current_timestamp = last_track_timestamp - 1
        time.sleep(0.25)  # Be nice to the API

    print(f"\nTotal tracks listened in 2024: {len(all_tracks)}")

    if all_tracks:
        print("\nFirst 5 tracks:")
        for track in all_tracks[:5]:
            print(f"{datetime.fromtimestamp(int(track.timestamp))} - {track.track.artist} - {track.track.title}")
        print("\nLast 5 tracks:")
        for track in all_tracks[-5:]:
            print(f"{datetime.fromtimestamp(int(track.timestamp))} - {track.track.artist} - {track.track.title}")
    else:
        print("No tracks found in this time period")

except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
