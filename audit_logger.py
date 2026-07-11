import pandas as pd
from pathlib import Path

class AuditLogger:
    def __init__(self):
        self.records = []

    def log_event(self, patient_folder: str, original_path: str, new_dcm_path: str, identity: dict, bbox: str):
        """Appends a successfully processed image to the audit trail."""
        self.records.append({
            "patient_folder": patient_folder,
            "original_file_path": original_path,
            "new_dcm_path": new_dcm_path,
            "synthetic_name": identity['name'],
            "synthetic_id": identity['id'],
            "synthetic_dob": identity['dob'],
            "bounding_box": bbox
        })

    def export_log(self, output_csv_path: Path):
        """Exports the aggregated audit trail to a CSV."""
        df = pd.DataFrame(self.records)
        df.to_csv(output_csv_path, index=False)
        print(f"✅ Audit log exported with {len(self.records)} records to: {output_csv_path}")
