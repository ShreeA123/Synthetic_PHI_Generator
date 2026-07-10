import hashlib
from faker import Faker

def generate_patient_identity(patient_folder_name: str) -> dict:
    """
    Generates a deterministic synthetic identity (Name, Patient ID, DOB) 
    based on the unique hash value of the patient's folder name/ID.
    """
    fake = Faker()
    
    # Create a stable numeric seed from the folder name (e.g., "Pt93.21")
    folder_seed = int(hashlib.sha256(patient_folder_name.encode('utf-8')).hexdigest(), 16) % 10**8
    fake.seed_instance(folder_seed)

    # Generate and return the variables in memory
    return {
        "name": fake.name(),
        "id": fake.bothify(text='ID-????####'),
        "dob": fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y%m%d')
    }