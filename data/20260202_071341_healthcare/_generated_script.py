import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from fpdf import FPDF

# Define output directory and create necessary folders
output_dir = "C:/Work/15_fabric_ontology/data/20260202_071341_healthcare"
config_dir = os.path.join(output_dir, "config")
tables_dir = os.path.join(output_dir, "tables")
documents_dir = os.path.join(output_dir, "documents")
os.makedirs(config_dir, exist_ok=True)
os.makedirs(tables_dir, exist_ok=True)
os.makedirs(documents_dir, exist_ok=True)

# Constants for data generation
NUM_PATIENTS = 16
NUM_APPOINTMENTS = 40

# Generate patient data
first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 
               'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
patients = pd.DataFrame({
    'patient_id': [f'PAT{str(i).zfill(3)}' for i in range(1, NUM_PATIENTS + 1)],
    'name': [f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(NUM_PATIENTS)],
    'date_of_birth': [(datetime.now() - timedelta(days=random.randint(365*20, 365*80))).strftime('%Y-%m-%d') for _ in range(NUM_PATIENTS)]
})

# Generate appointment data
appointment_types = random.choices(['Checkup', 'Urgent', 'Specialist', 'Lab'], weights=[40, 20, 25, 15], k=NUM_APPOINTMENTS)
wait_times = [random.randint(5, 60) for _ in range(NUM_APPOINTMENTS)]
durations = random.choices([15, 30, 45, 60], k=NUM_APPOINTMENTS)
appointments = pd.DataFrame({
    'appointment_id': [f'APPT{str(i).zfill(3)}' for i in range(1, NUM_APPOINTMENTS + 1)],
    'patient_id': [random.choice(patients['patient_id']) for _ in range(NUM_APPOINTMENTS)],
    'appointment_date': [(datetime.now() + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d') for _ in range(NUM_APPOINTMENTS)],
    'appointment_type': appointment_types,
    'actual_wait_minutes': wait_times,
    'duration_minutes': durations
})

# Write CSV files
patients.to_csv(os.path.join(tables_dir, 'patients.csv'), index=False)
appointments.to_csv(os.path.join(tables_dir, 'appointments.csv'), index=False)

# Create ontology config
config = {
    "scenario": "healthcare",
    "name": "Patient Records and Appointment Scheduling",
    "description": "Manage patient records and scheduling of appointments",
    "tables": {
        "patients": {
            "columns": ["patient_id", "name", "date_of_birth"],
            "types": {"patient_id": "String", "name": "String", "date_of_birth": "Date"},
            "key": "patient_id",
            "source_table": "patients"
        },
        "appointments": {
            "columns": ["appointment_id", "patient_id", "appointment_date", "appointment_type", "actual_wait_minutes", "duration_minutes"],
            "types": {"appointment_id": "String", "patient_id": "String", "appointment_date": "Date", "appointment_type": "String", "actual_wait_minutes": "BigInt", "duration_minutes": "BigInt"},
            "key": "appointment_id",
            "source_table": "appointments"
        }
    },
    "relationships": [
        {"name": "patient_appointment", "from": "patients", "to": "appointments", "fromKey": "patient_id", "toKey": "patient_id"}
    ]
}
with open(os.path.join(config_dir, 'ontology_config.json'), 'w') as f:
    json.dump(config, f, indent=4)

# Create sample questions
questions = """=== SQL QUESTIONS (Fabric Data) ===
- How many appointments were booked last month?
- What is the average wait time per appointment?
- Which patient has the most appointments?
- How many checkup appointments were scheduled?
- What is the total duration of appointments for each patient?

=== DOCUMENT QUESTIONS (AI Search) ===
- What is our maximum wait time policy?
- What are the scheduling requirements for appointments?
- How do we handle appointment cancellations?
- What identification is required for new patients?
- What are the follow-up procedures for patients?

=== COMBINED INSIGHT QUESTIONS ===
- Which patients exceeded the maximum wait time defined in our policy documents?
- How many appointments are overdue based on our scheduling requirements?
- What percentage of patients met our checkup appointment standards according to policy?
- Which appointments had wait times exceeding our defined thresholds in documents?
- Which patients are overdue for follow-up visits based on our policies?
"""
with open(os.path.join(config_dir, 'sample_questions.txt'), 'w') as f:
    f.write(questions)

# Create PDF policy documents
def create_pdf(title, sections, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(10)
    for heading, content in sections:
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, heading, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        content = content.encode('ascii', 'replace').decode('ascii')
        pdf.multi_cell(0, 6, content)
        pdf.ln(5)
    pdf.output(os.path.join(documents_dir, filename))

sections1 = [
    ("1. Appointment Scheduling", 
     "All appointments must be scheduled at least 24 hours in advance unless deemed urgent. Urgent cases must be communicated via phone. "
     "Patients who cancel appointments with less than 12 hours' notice may incur a cancellation fee."),
    ("2. Patient Registration Requirements",
     "New patients are required to bring valid identification, including a government-issued ID and proof of address. "
     "All necessary forms must be filled out accurately to ensure effective communication."),
    ("3. Wait Time Policy",
     "The maximum wait time for appointments should not exceed 30 minutes. Staff must monitor and communicate any delays promptly."),
    ("4. Follow-up Appointment Guidelines",
     "Patients are encouraged to schedule follow-up appointments before leaving the office. Follow-up visits should occur within 6 weeks "
     "of initial evaluation unless otherwise directed by the physician."),
    ("5. Cancellation Policy",
     "Patients should inform the office of cancellations as soon as possible. Cancellations made with less than 12 hours' notice will "
     "result in a fee of $25 for the first occurrence and $50 for any subsequent occurrences.")
]
create_pdf("Patient Appointment Policy", sections1, "patient_appointment_policy.pdf")

sections2 = [
    ("1. Emergency Procedures", 
     "In case of a medical emergency, patients are advised to call 911 immediately. "
     "The clinic will assist with referrals for emergency care where necessary."),
    ("2. Treatment Guidelines", 
     "All treatments must be documented and included in the patient's medical record. "
     "Patients should be informed of possible side effects and alternative treatments."),
    ("3. Medication Policies", 
     "Prescriptions must be filled within 7 days of issuance. Patients should schedule appointments to discuss any medication changes."),
    ("4. Telehealth Procedures", 
     "Telehealth services are available. Patients should provide a valid email to receive appointments and follow-up communications."),
    ("5. Patient Rights", 
     "Patients have the right to be informed about their treatment progress. "
     "Confidentiality will be maintained in compliance with HIPAA regulations.")
]
create_pdf("Patient Treatment and Rights Policy", sections2, "patient_treatment_rights_policy.pdf")

sections3 = [
    ("1. Health Information Privacy",
     "Patient health information is confidential and cannot be shared without consent. Employees must complete HIPAA training annually."),
    ("2. Medical Records Access",
     "Patients have rights to access their medical records upon submission of a written request. " 
     "Requests will be fulfilled within 30 days of receipt."),
    ("3. Appointment Reminders",
     "Patients will receive reminders for their appointments via SMS or email. " 
     "Reminders will be sent 48 hours before the scheduled appointment."),
    ("4. Insurance Requirements",
     "For services rendered, patients must provide correct insurance details prior to their appointment. "
     "Any changes to insurance must be communicated immediately."),
    ("5. Emergency Contact Information",
     "Patients are required to provide an emergency contact person in case of severe medical situations or emergencies. "
     "This information should be updated regularly.")
]
create_pdf("Patient Health Information Policy", sections3, "patient_health_information_policy.pdf")

print("Data generation and document creation completed successfully.")