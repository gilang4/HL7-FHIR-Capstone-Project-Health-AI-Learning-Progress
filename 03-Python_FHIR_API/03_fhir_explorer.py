import requests
import json

BASE_URL = "https://r4.smarthealthit.org"

# ── 1. GET PATIENT ──────────────────────────────────────
patient = requests.get(
        # The code visits the /Patient "room" at the FHIR address.
    f"{BASE_URL}/Patient",
    params={"_count": 5},
    headers={"Accept": "application/fhir+json"}
).json()

        # Parse out the first patient
        # digs through this wrapper (["entry"][0]["resource"]) to get to the actual patient data
p = patient["entry"][0]["resource"]
patient_id = p["id"]
patient_name = p["name"][0]["text"] if "text" in p["name"][0] else "Unknown"
        # if the birthdate is missing, it prints "Unknown" instead of crashing the script.
patient_dob = p.get("birthDate", "Unknown")

print(f"👤 Patient: {patient_name} | DOB: {patient_dob} | ID: {patient_id}")

# ── 2. GET CONDITIONS ────────────────────────────────────
conditions = requests.get(
    f"{BASE_URL}/Condition",
    params={"patient": patient_id, "_count": 10},
    headers={"Accept": "application/fhir+json"}
).json()

print("\n🏥 Conditions:")
for entry in conditions.get("entry", []):
    code = entry["resource"]["code"]["text"]
    print(f"  - {code}")

# ── 3. GET MEDICATIONS ───────────────────────────────────
meds = requests.get(
    f"{BASE_URL}/MedicationRequest",
    params={"patient": patient_id, "_count": 5},
    headers={"Accept": "application/fhir+json"}
).json()

print("\n💊 Medications:")
for entry in meds.get("entry", []):
    med = entry["resource"]["medicationCodeableConcept"]["text"]
    print(f"  - {med}")

# ── 4. SAVE TO JSON ──────────────────────────────────────
output = {
    "patient": {
        "id": patient_id,
        "name": patient_name,
        "dob": patient_dob
    },
    "conditions": [
        entry["resource"]["code"]["text"]
        for entry in conditions.get("entry", [])
    ],
    "medications": [
        entry["resource"]["medicationCodeableConcept"]["text"]
        for entry in meds.get("entry", [])
    ]
}

with open("patient_summary.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n✅ Saved to patient_summary.json")