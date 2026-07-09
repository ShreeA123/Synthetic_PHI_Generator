import datetime
import SimpleITK as sitk
import pydicom
from pathlib import Path

def format_to_dicom(temp_jpg_path: Path, out_dcm_path: Path, identity: dict):
    """
    Converts the temporary JPG into a compliant DICOM wrapper with the help 
    of SimpleITK and injects the synthetic identity into the metadata tags.
    """
    # 1. SimpleITK Conversion (Avoids all Numpy array shape errors)
    sitk_img = sitk.ReadImage(str(temp_jpg_path))
    sitk.WriteImage(sitk_img, str(out_dcm_path))

    # 2. Metadata Header Injection
    ds = pydicom.dcmread(str(out_dcm_path), force=True)
    
    ds.PatientName = identity['name']
    ds.PatientID = identity['id']
    ds.PatientBirthDate = identity['dob']
    ds.StudyDate = datetime.datetime.now().strftime('%Y%m%d')
    ds.Modality = 'US'
    ds.Manufacturer = 'SYNTHETIC-DEID-PIPELINE'
    
    ds.save_as(str(out_dcm_path))