import json
import shutil
from pathlib import Path

# --- Paths ---
video_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\01. Originals\No Overlay Videos")
merge_file = Path(r"C:\Users\nikhi\Documents\Coding\GitHub Repos\SnapchatMemoriesCaptionAdder\merge_candidates.json")
unmerged_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\02. Merged Videos\No Overlay Videos Unmerged")
unmerged_folder.mkdir(exist_ok=True)

# --- Load merge candidate groups ---
with open(merge_file, "r") as f:
    merge_groups = json.load(f)

# Flatten into a set of all filenames that are part of merges
merged_files = {f for group in merge_groups for f in group}

# --- Copy unmerged files ---
for video in video_folder.glob("*.mp4"):
    if video.name not in merged_files:
        dest = unmerged_folder / video.name
        shutil.copy2(video, dest)
        print(f"Copied {video.name} -> {dest}")

print("Done copying unmerged videos.")
