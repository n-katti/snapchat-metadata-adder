import json
import logging
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from typing import List, NamedTuple
import pytz
from dateutil.tz import tzlocal  # system timezone like pipeline

# --- Setup logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Paths ---
INPUT_FOLDER = "input"
JSON_FILE = Path(INPUT_FOLDER) / "memories_history.json"
OUTPUT_FILE = Path("merge_candidates.json")

# --- Minimal structures ---
class MediaType:
    Image = "image"
    Video = "video"

class Location(NamedTuple):
    latitude: float
    longitude: float

class VideoMetadata:
    def __init__(self, date: datetime, media_type: str, location: Location, mid: str):
        self.date = date
        self.type = media_type
        self.location = location
        self.mid = mid

    def filename(self):
        # Always use system local timezone (like pipeline)
        local_tz = tzlocal()
        local_date = self.date.astimezone(local_tz)
        return local_date.strftime("%Y-%m-%d_%H_%M_") + self.mid + ".mp4"

# --- Parse memories_history.json like processing pipeline ---
def parse_history(json_file: Path) -> List[VideoMetadata]:
    with json_file.open() as f:
        memory_entries = json.load(f)["Saved Media"]

    videos = []
    for entry in memory_entries:
        if entry["Media Type"].lower() != "video":
            continue

        mid = parse_qs(urlparse(entry["Download Link"]).query)["mid"][0]

        # Hardcode UTC to make aware datetime
        date = datetime.strptime(entry["Date"], "%Y-%m-%d %H:%M:%S UTC").replace(tzinfo=pytz.UTC)

        latitude, longitude = [
            float(numstr)
            for numstr in entry["Location"].removeprefix("Latitude, Longitude: ").split(", ")
        ]
        location = Location(latitude, longitude)

        videos.append(VideoMetadata(date=date, media_type="video", location=location, mid=mid))

    # 🔑 Sort everything upfront by date
    videos.sort(key=lambda v: v.date)
    return videos

# --- Grouping function ---
def group_videos_for_merge(metadata_list, time_delta_seconds=11, loc_delta=0.0001):
    videos = [m for m in metadata_list if m.type == "video"]
    grouped = []
    used = set()
    for i, vid in enumerate(videos):
        if vid in used:
            continue
        cluster = [vid]
        used.add(vid)
        for other in videos[i + 1:]:
            if other in used:
                continue
            # ✅ compare to the last item in the cluster, not the first
            last = cluster[-1]
            time_diff = abs((other.date - last.date).total_seconds())
            lat_diff = abs(other.location.latitude - last.location.latitude)
            lon_diff = abs(other.location.longitude - last.location.longitude)
            if time_diff <= time_delta_seconds and lat_diff <= loc_delta and lon_diff <= loc_delta:
                cluster.append(other)
                used.add(other)
            else:
                break  # since list is sorted, no point checking further
        grouped.append(cluster)
    return grouped


# --- Main ---
def main():
    if not JSON_FILE.exists():
        logging.error(f"Cannot find {JSON_FILE}")
        return

    metadata_list = parse_history(JSON_FILE)

    grouped_videos = group_videos_for_merge(metadata_list)
    merge_candidates = [g for g in grouped_videos if len(g) > 1]

    merge_data = []
    if merge_candidates:
        logging.info(f"Total groups of videos to merge: {len(merge_candidates)}")
        for i, group in enumerate(merge_candidates, start=1):
            filenames = [v.filename() for v in group]
            merge_data.append(filenames)
            logging.info(f"Group {i}: {filenames}")
        with open(OUTPUT_FILE, "w") as f:
            json.dump(merge_data, f, indent=4)
        logging.info(f"Merge candidate list saved to {OUTPUT_FILE}")
    else:
        logging.info("No videos need to be merged.")

if __name__ == "__main__":
    main()
