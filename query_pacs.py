import os
import argparse
import pydicom
import logging
import time
import subprocess
from pynetdicom import AE, evt, StoragePresentationContexts
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind


# Constants for the retry mechanism
MAX_RETRIES = 55
BACKOFF_FACTOR = 2
INITIAL_WAIT = 60

# DICOM Network Configuration
AE_TITLE = 'YOUR_AE_TITLE'
AE_CALLED_TITLE = 'RADIOLOGY'
PACS_ADDR = '127.0.0.1'
PACS_PORT = 12005

DICOM_PATH = os.path.join(os.getcwd(), 'studies')

def handle_store(event):
    """Handle a C-STORE request event."""
    try:
        ds = event.dataset
        # Set file path
        file_path = os.path.join(DICOM_PATH, ds.AccessionNumber, ds.SOPInstanceUID + ".dcm")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Save DICOM file
        ds.save_as(file_path, write_like_original=False)
        return 0x0000  # Success status
    except Exception as e:
        logging.error(f"Error in handle_store: {e}")
        return 0xC001  # Some failure status

def query_study_info(patient_id: str):
    """Query study descriptions and dates for a given patient ID."""
    study_info = []
    ae = AE(ae_title=AE_TITLE)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

    for _ in range(MAX_RETRIES):
        try:
            assoc = ae.associate(PACS_ADDR, PACS_PORT, ae_title=AE_CALLED_TITLE)
            if assoc.is_established:
                # Create and send C-FIND request
                ds = pydicom.Dataset()
                ds.PatientID = patient_id
                ds.QueryRetrieveLevel = 'STUDY'
                ds.StudyDescription = ''  # Request the StudyDescription
                ds.StudyDate = ''  # Request the StudyDate
                responses = assoc.send_c_find(ds, PatientRootQueryRetrieveInformationModelFind)
                for (status, identifier) in responses:
                    if status and identifier:
                        desc = identifier.get('StudyDescription', 'No Description')
                        date = identifier.get('StudyDate', 'No Date')
                        study_info.append((desc, date))
                assoc.release()
                return study_info
            else:
                raise RuntimeError("Could not establish association with PACS")
        except Exception as e:
            wait_time = INITIAL_WAIT * (BACKOFF_FACTOR ** _)
            logging.warning(f"Attempt {_ + 1} failed: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    return study_info

def construct_task_command(study_info, reference_study):
    """Constructs the task command for ollama."""
    # Format each study description and date
    formatted_studies = [f"{desc}, {date}" for desc, date in study_info]
    # Create a comma-separated list of studies
    study_list = ", ".join(formatted_studies)
    task = f'"COMPARISON: {study_list}. Take this list of radiological studies and create a short comma-separated list of the most relevant studies based on anatomical region and date, compared to the following study: {reference_study}."'
    command = f"ollama run mistral {task}"
    return command


def main(patient_id: str, reference_study: str):
    study_info = query_study_info(patient_id)
    if study_info:
        command = construct_task_command(study_info, reference_study)
        # Execute the command
        subprocess.run(command, shell=True)
    else:
        print("No studies found or an error occurred.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Query study information from PACS and process with mistral.')
    parser.add_argument('patient_id', type=str, help='Patient ID to query study information')
    parser.add_argument('reference_study', type=str, help='Reference study for comparison')
    args = parser.parse_args()
    main(args.patient_id, args.reference_study)
