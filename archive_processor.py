import zipfile
from pathlib import Path

def process_archives(root_path: Path):
    """
    Traverses the root directory to find and extract compressed image batches.
    While safely ignoring system files and already extracted folders.
    """
    for patient_dir in root_path.iterdir():
        if not patient_dir.is_dir() or patient_dir.name == ".DS_Store":
            continue

        zip_candidates = []
        for p in patient_dir.iterdir():
            if p.name == ".DS_Store":
                continue
            
            # Match files like processed_<digits>_images_batch
            if p.name.startswith("processed_") and "images_batch" in p.name:
                zip_candidates.append(p)

        for candidate in zip_candidates:
            if candidate.is_dir():
                continue

            out_folder = candidate.with_name(candidate.stem)
            
            try:
                with zipfile.ZipFile(candidate, "r") as z:
                    # Skip if already extracted
                    if out_folder.exists() and any(out_folder.iterdir()):
                        continue
                    out_folder.mkdir(parents=True, exist_ok=True)
                    z.extractall(out_folder)
            except zipfile.BadZipFile:
                continue