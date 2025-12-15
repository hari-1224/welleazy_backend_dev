from django.apps import apps

def filter_record_for_compare(data):

    # Remove metadata fields
    remove_fields = [
        "id",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "deleted_at",
        "record",
        "category",    
    ]

    for key in remove_fields:
        data.pop(key, None)
        
    for key, value in data.items():
        if isinstance(value, str):
            data[key] = value.strip()

    # Clean parameters
    if "parameters" in data:
        cleaned_params = []
        for p in data["parameters"]:
            cleaned = {
                "parameter_name": p.get("parameter_name"),
                "result": p.get("result"),
                "unit": p.get("unit"),
                "start_range": p.get("start_range"),
                "end_range": p.get("end_range"),
            }
            cleaned_params.append(cleaned)
        data["parameters"] = cleaned_params

    # Clean documents
    if "documents" in data:
        cleaned_docs = []
        for d in data["documents"]:
            cleaned_docs.append({
                "file": d.get("file")   # do NOT compare ID or timestamps
            })
        data["documents"] = cleaned_docs
        
    if "schedule_times" in data:
        cleaned_times = []
        for t in data["schedule_times"]:
            cleaned_times.append({
                "time": t.get("time")
            })
        data["schedule_times"] = cleaned_times

    return data

def get_model_from_module(module_name: str):
    mapping = {
        "prescriptions": "prescriptions.PrescriptionRecord",
        "hospitalizations": "hospitalizations.HospitalizationRecord",
        "medical_bills": "medical_bills.MedicalBillRecord",
        "vaccination_certificates": "vaccination_certificates.VaccinationCertificateRecord",
        "medicine_reminders": "medicine_reminders.MedicineReminder",
        
        # Health metrics
        "height": "health.HeightRecord",
        "weight": "health.WeightRecord",
        "bmi": "health.BmiRecord",
        "blood_pressure": "health.BloodPressureRecord",
        "heart_rate": "health.HeartRateRecord",
        "oxygen": "health.OxygenSaturationRecord",
        "glucose": "health.GlucoseRecord",
    }

    if module_name not in mapping:
        raise ValueError(f"Invalid module name: {module_name}")

    return apps.get_model(mapping[module_name])


def dict_diff(records: list[dict]):
    keys = set().union(*records)
    diff = {}

    for key in keys:
        values = [rec.get(key) for rec in records]

        # Normalize to string, trim spaces, lower case
        normalized = [
            str(v).strip().lower() if isinstance(v, str) else v
        for v in values]

        # Detect if normalized values differ
        if len(set([str(v) for v in normalized])) > 1:
            diff[key] = values  

    return diff

