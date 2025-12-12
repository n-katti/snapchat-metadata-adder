import json
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips

# --- Paths ---
video_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\Test")
merge_file = Path(r"C:\Users\nikhi\Documents\Coding\GitHub Repos\SnapchatMemoriesCaptionAdder\merge_candidates.json")
output_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\Test\Merge")
output_folder.mkdir(exist_ok=True)

# --- Load merge candidate groups ---
with open(merge_file, "r") as f:
    merge_groups = json.load(f)

def merge_videos(group_files, output_path):
    """
    Merge multiple videos using MoviePy with higher quality.
    """
    clips = [VideoFileClip(f) for f in group_files]
    final_clip = concatenate_videoclips(clips, method="compose")

    # Export with higher quality settings
    final_clip.write_videofile(
        str(output_path),
        codec="libx264",
        audio_codec="aac",
        preset="slow",
        bitrate="8000k",
        audio_bitrate="192k",
        fps=30,
        threads=4,
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        logger="bar"     
    )

    # Close clips to release memory
    for clip in clips:
        clip.close()
    final_clip.close()

    print(f"Merged {len(group_files)} videos into {output_path.name}")

# --- Process each group ---
for i, group in enumerate(merge_groups, start=1):
    files = [video_folder / f for f in group]

    missing = [f.name for f in files if not f.exists()]
    if missing:
        print(f"Skipping group {i} because some files are missing: {missing}")
        continue

    first_file = files[0]
    merged_name = first_file.stem + "_merged.mp4"
    output_path = output_folder / merged_name

    merge_videos(files, output_path)
