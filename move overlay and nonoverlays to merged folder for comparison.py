import shutil
from pathlib import Path

# --- Adjust these paths ---
media_type = "Pictures"
# base_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat")  # parent folder containing both source folders
# with_overlay_folder = base_folder / f"Overlay {media_type}"
# without_overlay_folder = base_folder / f"Overlay {media_type} Without Overlay"
# merged_folder = base_folder / f"Merged {media_type}"

with_overlay_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\02. Merged Videos\Overlay Videos Merged")
without_overlay_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\02. Merged Videos\Overlay Videos Without Overlay Merged")
merged_folder = Path(r"C:\Users\nikhi\Pictures\Snapchat\03. Reconciled\Reconciled Overlay Videos")

# Create Merged folder if it doesn't exist
merged_folder.mkdir(exist_ok=True)

# --- Copy files without overlay ---
for file_path in without_overlay_folder.iterdir():
    if file_path.is_file():
        shutil.copy(file_path, merged_folder / file_path.name)

# --- Copy files with overlay, append _01 ---
for file_path in with_overlay_folder.iterdir():
    if file_path.is_file():
        new_name = file_path.stem + "_01" + file_path.suffix
        shutil.copy(file_path, merged_folder / new_name)

print(f"All files copied to {merged_folder}")
