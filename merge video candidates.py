import json
import subprocess
from pathlib import Path

# --- Paths ---
# video_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\01. Originals\No Overlay Videos")
video_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\Test")
merge_file = Path(r"C:\Users\nikhi\Documents\Coding\GitHub Repos\SnapchatMemoriesCaptionAdder\merge_candidates.json")
# output_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\02. Merged Videos\No Overlay Videos Merged")
output_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\Test\Merge")
output_folder.mkdir(exist_ok=True)

# --- Load merge candidate groups ---
with open(merge_file, "r") as f:
    merge_groups = json.load(f)

def merge_videos(group_files, output_path):
    """
    Merge multiple videos using ffmpeg with re-encode to avoid stutters.
    """
    concat_file = output_path.with_suffix(".txt")
    with open(concat_file, "w", encoding="utf-8") as cf:
        for f in group_files:
            cf.write(f"file '{f.as_posix()}'\n")

    cmd = [
        "ffmpeg", "-y",                        # overwrite without asking
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-crf", "18",       # high quality H.264
        "-preset", "fast",                     # faster encoding
        "-c:a", "aac", "-b:a", "192k",         # AAC audio
        "-movflags", "+faststart",             # web-friendly playback
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    concat_file.unlink()
    print(f"Merged {len(group_files)} videos into {output_path.name}")

# --- Process each group ---
for i, group in enumerate(merge_groups, start=1):
    files = [video_folder / f for f in group]

    # Skip the group if any file is missing
    missing = [f.name for f in files if not f.exists()]
    if missing:
        print(f"Skipping group {i} because some files are missing: {missing}")
        continue

    first_file = files[0]
    merged_name = first_file.stem + "_merged.mp4"
    output_path = output_folder / merged_name

    merge_videos(files, output_path)
