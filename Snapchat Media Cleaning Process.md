# Snapchat Media Cleaning Process

## 1. Initial Setup
- Installed **FFmpeg** and **VIPS**.
- Downloaded all Snapchat data.

## 2. Separate Overlays
- Ran `separate overlay and no overlay.py` to separate media into:
  - Images with overlays  
  - Images without overlays  
  - Videos with overlays  
  - Videos without overlays  
- Created “super raw” folders for each category.

## 3. Add Metadata
- Ran **SnapchatMetaDataAdder** six times:
  1. Images without overlays  
  2. Videos without overlays  
  3. Images with overlays **including** overlays  
  4. Videos with overlays **including** overlays  
  5. Images with overlays **excluding** overlays  
  6. Videos with overlays **excluding** overlays  

- All outputs moved into `/01. Originals`, organized as:
  - `No Overlay Pictures`  
  - `No Overlay Videos`  
  - `Overlay Pictures`  
  - `Overlay Videos`  
  - `Overlay Pictures Without Overlay`  
  - `Overlay Videos Without Overlay`

# Pictures 
## Pictures Without Overlays
  - Go through `/01. Originals/No Overlay Pictures` and keep/delete pictures
  - The output of this step should be placed in `/03. Reconciled/No Overlay Pictures`


## Pictures With Overlays
  - Run `move overlay and nonoverlays to merged folder for comparison.py` on `01. Originals/Overlay Pictures` and `01. Originals/Overlay Pictures Without Overlay`
  - This moves overlay pictures with their overlays and overlay pictures without their overlays into a Merged Pictures folder
  - From this folder, go through and keep/delete any pictures
  - The output of this step should be placed in `/03. Reconciled/Overlay Pictures`


# Videos

## Identify Merge Candidates
- Run `find_merged_files.py` on:
  - `01. Originals/No Overlay Videos`
  - `01. Originals/Overlay Videos`
  - `01. Originals/Overlay Videos Without Overlays`
- This uses location and timestamp to generate `merge_candidates.json` containing the file names of all videos that should be merged
  - Snapchat splits videos longer than 10 seconds up into 10 seconds increments

## Merge Videos
- Run `merge_video_candidates.py` on: 
  - `01. Originals/No Overlay Videos`
  - `01. Originals/Overlay Videos`
  - `01. Originals/Overlay Videos Without Overlays`
- The output of this step is placed in:
  - `02. Merged Videos/No Overlay Videos Merged`
  - `02. Merged Videos/Overlay Videos Merged`
  - `02. Merged Videos/Overlay Videos Without Overlays Merged`

## Move Non-Merged Videos
- Run `move nonmerged videos.py` on:
  - `01. Originals/No Overlay Videos`
  - `01. Originals/Overlay Videos`
  - `01. Originals/Overlay Videos Without Overlays`
- This moves all videos that were not identified in `merge_candidates.json` to:
  - `02. Merged Videos/No Overlay Videos Unmerged`
  - `02. Merged Videos/Overlay Videos Unmerged`
  - `02. Merged Videos/Overlay Videos Without Overlays Unmerged`
  

## Combine the above two steps
- Combine the following folders:
  - Move `02. Merged Videos/No Overlay Videos Unmerged` into `02. Merged Videos/No Overlay Videos Merged`
  - Move `02. Merged Videos/Overlay Videos Unmerged` into `02. Merged Videos/Overlay Videos Merged`
  - Move `02. Merged Videos/Overlay Videos Without Overlays Unmerged` into `02. Merged Videos/Overlay Videos Without Overlays Merged`

- You will end up with 3 final folders with all videos

## Videos With Overlays
  - Run `move overlay and nonoverlays to merged folder for comparison.py` on `02. Merged Videos/Overlay Videos` and `02. Merged Videos/Overlay Videos Without Overlay`
  - This moves overlay videos with their overlays and overlay videos without their overlays into `03. Reconciled\Reconciled Overlay Videos`
  - From this folder, go through and keep/delete any videos
  - The output of this step should be placed in `03. Reconciled\Reconciled Overlay Videos`

## Videos Without Overlays
- Go through and review and deleted unwanted videos from **02. Merged Videos/No Overlay Videos Merged**
- The output of this step should be placed in `03. Reconciled\Reconciled No Overlay Videos`


# Final Output
- Resulting folders contain the **final set of images and videos** ready for upload to Google Photos. The following four folders should be the final: 
  - Reconciled No Overlay Pictures
  - Reconciled No Overlay Videos
  - Reconciled Overlay Pictures
  - Reconciled Overlay Videos
