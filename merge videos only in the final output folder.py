import json
import subprocess
import os
from pathlib import Path

# --- Paths ---
base_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\01. Originals\No Overlay Videos")  # original videos
merge_file = Path(r"C:\Users\nikhi\Documents\Coding\GitHub Repos\SnapchatMemoriesCaptionAdder\merge_candidates.json")
final_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\03. Reconciled\Reconciled No Overlay Videos")  # current final output
process_output_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\Test\Merge_Intermediate")  # new merged outputs
final_folder.mkdir(exist_ok=True)
process_output_folder.mkdir(exist_ok=True)

EXIFTOOL = r"C:\Windows\System32\Exiftools\exiftool.exe"

# --- Load merge candidate groups ---
with open(merge_file, "r") as f:
    merge_groups = json.load(f)

# --- Step 0: Identify base filenames from kept merged videos ---
kept_merged_bases = [
    f.stem.replace("_merged", "") 
    for f in final_folder.glob("*_merged.mp4")
]
print("Kept merged video bases:", kept_merged_bases)

def merge_videos(group_files, output_path):
    concat_file = output_path.with_suffix(".txt")
    with open(concat_file, "w", encoding="utf-8") as cf:
        for f in group_files:
            cf.write(f"file '{f.as_posix()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c:v", "libx264", "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    concat_file.unlink()

def copy_embedded_metadata(src: Path, dst: Path):
    cmd = [
        EXIFTOOL,
        "-TagsFromFile", str(src),
        "-all:all",
        "-overwrite_original",
        str(dst),
    ]
    print("Running EXIFTOOL command:", cmd)
    subprocess.run(cmd, check=True)

def copy_filesystem_timestamps(source_file, target_file):
    stat = source_file.stat()
    os.utime(target_file, (stat.st_atime, stat.st_mtime))

# --- Process each group ---
for i, group in enumerate(merge_groups, start=1):
    first_file_name = group[0]
    if first_file_name.replace(".mp4", "") not in kept_merged_bases:
        print(f"Skipping group {i}: first file not in kept list")
        continue

    files = [base_folder / f for f in group]

    # Skip the group if any file is missing
    missing = [f.name for f in files if not f.exists()]
    if missing:
        print(f"Skipping group {i} because some files are missing: {missing}")
        continue

    first_file = files[0]
    merged_name = first_file.stem + "_merged.mp4"
    output_path = process_output_folder / merged_name  # merge into intermediate/process folder

    merge_videos(files, output_path)
    copy_embedded_metadata(first_file, output_path)
    copy_filesystem_timestamps(first_file, output_path)

    print(f"Merged {len(files)} videos with metadata + timestamps preserved → {merged_name}")
