import shutil
from pathlib import Path

# Paths
input_path = Path(r"C:\Users\nikhi\Downloads\mydata~1755985226030\memories")
output_path = Path(r"C:\Users\nikhi\Downloads\mydata~1755985226030\separated memories")

# Output directories
with_overlay_video_path = output_path / "with_overlay_video"
without_overlay_video_path = output_path / "without_overlay_video"
with_overlay_image_path = output_path / "with_overlay_image"
without_overlay_image_path = output_path / "without_overlay_image"

# Create output directories if they don't exist
for path in [with_overlay_video_path, without_overlay_video_path, with_overlay_image_path, without_overlay_image_path]:
    path.mkdir(parents=True, exist_ok=True)

# Gather all files
files = list(input_path.glob("*.*"))

# Map files by their base name (without -main/-overlay)
media_map = {}
for file in files:
    stem = file.stem
    if stem.endswith("-main"):
        key = stem[:-5]  # remove '-main'
        media_map.setdefault(key, {})["main"] = file
    elif stem.endswith("-overlay"):
        key = stem[:-8]  # remove '-overlay'
        media_map.setdefault(key, {})["overlay"] = file
    else:
        media_map.setdefault(stem, {})["main"] = file

# Process the mapping
for key, value in media_map.items():
    main_file = value.get("main")
    overlay_file = value.get("overlay")

    # Determine type
    if main_file and main_file.suffix.lower() == ".mp4":
        # Video
        if main_file and overlay_file:
            shutil.copy2(main_file, with_overlay_video_path / main_file.name)
            shutil.copy2(overlay_file, with_overlay_video_path / overlay_file.name)
        elif main_file:
            shutil.copy2(main_file, without_overlay_video_path / main_file.name)
    else:
        # Image
        if main_file and overlay_file:
            shutil.copy2(main_file, with_overlay_image_path / main_file.name)
            shutil.copy2(overlay_file, with_overlay_image_path / overlay_file.name)
        elif main_file:
            shutil.copy2(main_file, without_overlay_image_path / main_file.name)

    # Handle overlay without main
    if overlay_file and not main_file:
        print(f"⚠️ Overlay without main found: {overlay_file.name}")
        # Decide where to put it based on extension
        if overlay_file.suffix.lower() == ".mp4":
            shutil.copy2(overlay_file, with_overlay_video_path / overlay_file.name)
        else:
            shutil.copy2(overlay_file, with_overlay_image_path / overlay_file.name)
