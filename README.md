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

## Dataset Overview
- Source: Stanford Lung Database (OpenPOCUS).
- Scope: 226 adult patients, 1,871 lung ultrasound video clips, and over 324,000 individual frames.
- Clinical Findings: Normal scans, B-lines, and subpleural consolidations representing both COVID-19 and non-COVID pathologies.

## Data Set Location Format
The downloaded Stanford Lung Database follows a nested directory structure that must be parsed:
-  Root Directory: Contains ~226 individual patient folders (e.g., Pt93.21, Pt94.1)

-  Batch Zips: Inside patient folders, images are frequently compressed into archives named with the prefix processed_<number>_images_batch.zip

-  Direct Images: Some patient folders do not contain nested batches and instead house .jpg or .png ultrasound frames directly in the root of the patient folder

-  Metadata: Each batch contains a meta data.csv mapping the images to their clinical labels

## Download links for the Dataset
- https://stanfordmedicine.app.box.com/s/ajv4y3fv5i6mhs345mwhbvkg80cuvzcc
- https://github.com/kumarandre/OpenPOCUS

## Tech Stack
- Language: Python
- Environment/IDE: VS Code
- Dataset Processing/Orchestration: Modular Python scripts + `pipeline_manager.py`
- Data Processing: pandas library
- Image Manipulation: pillow (PIL) library
- Medical Imaging / DICOM Creation: SimpleITK
- DICOM Metadata Injection: pydicom library
- Audit/Export Outputs: CSV via `audit_logger.py`
- Synthetic Identity Generation: Deterministic Hashing via `identity_simulator.py`

# Installation & Setup
It is recommended to run this pipeline within a virtual environment to prevent dependency conflicts with your system's global Python installation.
1.Create and activate a virtual environment: 
**Windows**  
- `python -m venv synth_data_gen`
- - `.\enterprise_deid\Scripts\activate`

**Mac/Linux**  
- `python3 -m venv enterprise_deid`
- - `source enterprise_deid/bin/activate`

2.Install dependencies: Install the required packages using the provided requirements.txt file:
`pip install -r requirements.txt`
## Usage
1.Open pipeline_manager.py in your text editor.

2.Update the Global Path Configurations at the top of the file to point to your local directories:
   - INPUT_ROOT: The extracted OpenPOCUS dataset folder.
   - OUTPUT_ROOT: The destination folder for the generated .dcm files and CSV audit log.
3.Execute the pipeline:
`python pipeline_manager.py`
## Storage Limitations & Batch Execution
**Storage Requirement**: The full OpenPOCUS dataset contains over 324,000 image frames. Executing the entire pipeline on the complete dataset will generate a massive amount of DICOM files, resulting in a minimum expected output size of 250 to 400 GB. Ensure your target drive has adequate storage space before running the full pipeline.
If you have limited disk space, or if you simply want to generate a smaller sample dataset (e.g., 20, 50, or 100 patients), you can easily modify the orchestrator to halt execution after a specific number of patient folders have been processed.
### How to limit the execution:
Open your `python pipeline_manager.py` file and locate the `run_pipeline()` function.
Add the counter and limit variables immediately before the main folder iteration loop (around line 24), and add the break condition immediately inside the loop:
    print("\n=== Phase 2: Pipeline Execution ===")
    
    # --- ADD THESE TWO LINES HERE ---
    processed_count = 0
    MAX_PATIENTS = 95  # Change this to 20, 50, etc. based on your storage capacity

    for patient_folder in INPUT_ROOT.iterdir():
        if not patient_folder.is_dir() or patient_folder.name == ".DS_Store":
            continue

        # --- ADD THIS CHECK BLOCK HERE ---
        if processed_count >= MAX_PATIENTS:
            print(f"\n⏹ Reached the limit of {MAX_PATIENTS} patients. Stopping generation to save disk space.")
            break
        processed_count += 1
        # ---------------------------------

        patient_folder_name = patient_folder.name
        # ... [Rest of the existing code remains unchanged] ...
By implementing this snippet, the pipeline will safely complete the selected number of patients, wrap up the processes, and successfully export the `master_phi_ground_truth.csv` for just those patients without overflowing your hard drive.
## Understanding DICOM & PHI
Digital Imaging and Communications in Medicine (DICOM) is the global technical standard for storing and transmitting medical images. Unlike a standard .jpg which only contains pixels, a .dcm file securely groups the pixel data together with a highly structured list of metadata "headers".
These headers contain explicit Protected Health Information (PHI) such as Patient's Name, Patient ID, and Birth Date, as well as indirect identifiers like Device Serial Number. To comply with the HIPAA Privacy Rule's Safe Harbor method, 18 specific categories of identifiers must be removed or sanitized from these headers. This pipeline programmatically injects synthetic PHI into these headers to simulate the real-world challenge of scrubbing them.
