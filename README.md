
# 🚀 Synthetic PHI Generation from Grayscale Ultrasound (Sonography) images in B‑mode (Brightness mode):
- This project provides a modular pipeline to generate realistic, privacy-safe synthetic Protected Health Information (PHI) for medical imaging, AI training and validation from Stanford Lung Database.
- Medical images inherently suffer from the "iceberg problem"—sensitive identifiers are not only visible as burned-in text on the image pixels but are also hidden deep within structural metadata (like DICOM headers). Because real patient data is heavily restricted by privacy laws like HIPAA, sharing authentic data to test AI de-identification models is legally challenging.
- This pipeline solves this by injecting clean, open-source ultrasound images with highly realistic, deterministically generated synthetic patient identities. By adhering to the HIPAA Safe Harbor method principles, this system creates a robust, perfect "ground truth" answer key for benchmarking optical character recognition (OCR) and redaction models.

## 📦 Table of Contents
- Architecture & Modules
- Dataset Overview
- Data Set Location Format
- Download links for the Dataset
- Installation & Setup
- Usage
- Storage Limitations & Batch Execution
- Understanding DICOM & PHI

## 🛠 Architecture & Modules 
To ensure scalability and maintainability, this project utilizes a modular architecture rather than a single monolithic script.
1.`archive_processor.py`: Handles data ingestion. It safely unzips nested patient batch archives while ignoring system files (like .DS_Store).
2.`identity_simulator.py`:The Identity Engine. Generates a deterministic synthetic identity (Name, ID, DOB) using a mathematical hash of the patient's folder name. This ensures all images for a specific patient receive the exact same identity.
3.`visual_injector.py`: The Visual Module. Evaluates pixel brightness to avoid obscuring clinical anatomy (like the ultrasound fan) and uses PIL to safely burn synthetic text into the image margins.
4.`dicom_formatter.py`: The Medical Formatter. Uses SimpleITK to convert modified .jpg/.png files into compliant .dcm files, and pydicom to inject the synthetic identity directly into the DICOM metadata headers.
5.`audit_logger.py`: The Audit Trail. Aggregates the actions taken and exports the master ground-truth CSV answer key.
6.`pipeline_manager.py`: The Master Orchestrator. The main executable that imports the modules above, maps paths, and orchestrates the end-to-end execution.

