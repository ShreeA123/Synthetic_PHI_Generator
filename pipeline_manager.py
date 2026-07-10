import os
from pathlib import Path

# Import custom module files
from archive_processor import process_archives
from identity_simulator import generate_patient_identity
from visual_injector import inject_visual_phi
from dicom_formatter import format_to_dicom
from audit_logger import AuditLogger

# --- GLOBAL PATH CONFIGURATION ---
INPUT_ROOT = Path(r"D:\Work\Synth_PHI_02\Database_02")
OUTPUT_ROOT = Path(r"E:\CVD\Synthetic_PHI_Dataset_02")

def run_pipeline():
    # Initialize infra
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    logger = AuditLogger()

    print("=== Phase 1: Archive Extraction ===")
    process_archives(INPUT_ROOT)

    print("\n=== Phase 2: Pipeline Execution ===")
    for patient_folder in INPUT_ROOT.iterdir():
        if not patient_folder.is_dir() or patient_folder.name == ".DS_Store":
            continue

        patient_folder_name = patient_folder.name
        
        # 1. Generate identity for this specific patient
        identity = generate_patient_identity(patient_folder_name)
        
        # 2. Create the patient's output directory
        patient_out_dir = OUTPUT_ROOT / patient_folder_name
        patient_out_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Processing Folder: {patient_folder_name} -> Synthetic Identity: {identity['name']}")

        for image_path in patient_folder.rglob("*.*"):
            if image_path.suffix.lower() not in ['.jpg', '.png']:
                continue

            out_dcm_path = patient_out_dir / f"{image_path.stem}.dcm"
            temp_jpg_path = patient_out_dir / f"temp_{image_path.name}"

            # 3. Visual PHI Burn-in
            bbox = inject_visual_phi(image_path, identity, temp_jpg_path)
            if not bbox:
                continue # Image skipped due to safety check

            # 4. DICOM Formatting & Header Injection
            try:
                format_to_dicom(temp_jpg_path, out_dcm_path, identity)
                temp_jpg_path.unlink() # Delete temporary JPG
            except Exception as e:
                print(f"  ⚠️ Error formatting DICOM for {image_path.name}: {e}")
                if temp_jpg_path.exists():
                    temp_jpg_path.unlink()
                continue

            # 5. Log the success to the Audit Trail
            logger.log_event(
                patient_folder=patient_folder_name,
                original_path=str(image_path),
                new_dcm_path=str(out_dcm_path),
                identity=identity,
                bbox=bbox
            )

    print("\n=== Phase 3: Audit Export ===")
    logger.export_log(OUTPUT_ROOT / "master_phi_ground_truth.csv")
    print("\n🎉 Pipeline Execution Complete!")

if __name__ == "__main__":
    run_pipeline()