# import shutil
# from pathlib import Path

# # Paths
# input_path = Path(r"C:\Users\nikhi\Downloads\mydata~1755985226030\memories")
# output_path = Path(r"C:\Users\nikhi\Downloads\mydata~1755985226030\separated memories")
# with_overlay_path = output_path / "with_overlay"
# without_overlay_path = output_path / "without_overlay"

# # Create output directories if they don't exist
# output_path.mkdir(parents=True, exist_ok=True)
# with_overlay_path.mkdir(parents=True, exist_ok=True)
# without_overlay_path.mkdir(parents=True, exist_ok=True)

# # Gather all files
# files = list(input_path.glob("*.*"))

# # Map files by their base name (without -main/-overlay)
# media_map = {}
# for file in files:
#     stem = file.stem
#     if stem.endswith("-main"):
#         key = stem[:-5]  # remove '-main'
#         media_map.setdefault(key, {})["main"] = file
#     elif stem.endswith("-overlay"):
#         key = stem[:-8]  # remove '-overlay'
#         media_map.setdefault(key, {})["overlay"] = file
#     else:
#         # Files that are neither main nor overlay
#         media_map.setdefault(stem, {})["main"] = file

# # Process the mapping
# for key, value in media_map.items():
#     main_file = value.get("main")
#     overlay_file = value.get("overlay")

#     if main_file and overlay_file:
#         # Both exist -> copy to with_overlay
#         shutil.copy2(main_file, with_overlay_path / main_file.name)
#         shutil.copy2(overlay_file, with_overlay_path / overlay_file.name)
#     elif main_file and not overlay_file:
#         # Only main exists -> copy to without_overlay
#         shutil.copy2(main_file, without_overlay_path / main_file.name)
#     elif overlay_file and not main_file:
#         # Only overlay exists -> flag it
#         print(f"⚠️ Overlay without main found: {overlay_file.name}")
#         # Optionally copy it to with_overlay anyway
#         shutil.copy2(overlay_file, with_overlay_path / overlay_file.name)

from datetime import datetime, timezone
from timezonefinderL import TimezoneFinder
from zoneinfo import ZoneInfo  # stdlib in Python 3.9+

def test_timezone(lat, lon, dt_utc):
    tf = TimezoneFinder()
    
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if tz_name:
        local_tz = ZoneInfo(tz_name)
        local_dt = dt_utc.astimezone(local_tz)
        print(f"Found timezone: {tz_name}")
    else:
        local_dt = dt_utc.astimezone()  # fallback to system local timezone
        print("Timezone not found, using system local timezone")
    
    print("UTC datetime:", dt_utc)
    print("Local datetime:", local_dt)

if __name__ == "__main__":
    # Example test
    test_lat = 38.4722    # New York latitude
    test_lon = -105.3555   # New York longitude
    dt_utc = datetime(2025, 8, 23, 12, 0, 0, tzinfo=timezone.utc)
    
    test_timezone(test_lat, test_lon, dt_utc)
