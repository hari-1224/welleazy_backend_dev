from django.apps import apps
from statistics import mean
from collections import Counter
from .unit_converter import normalize_value
from django.utils import timezone

def get_model_from_module(module_name: str):

    mapping = {
        # Health Records
        "height": "health.HeightRecord",
        "weight": "health.WeightRecord",
        "bmi": "health.BmiRecord",
        "blood_pressure": "health.BloodPressureRecord",
        "heart_rate": "health.HeartRateRecord",
        "oxygen": "health.OxygenSaturationRecord",
        "glucose": "health.GlucoseRecord",

        # Others
        "prescriptions": "prescriptions.PrescriptionRecord",
        "hospitalizations": "hospitalizations.HospitalizationRecord",
        "medical_bills": "medical_bills.MedicalBillRecord",
        "vaccination_certificates": "vaccination_certificates.VaccinationCertificateRecord",
        "medicine_reminders": "medicine_reminders.MedicineReminder",
    }

    if module_name not in mapping:
        raise ValueError(f"Invalid module name: {module_name}")

    return apps.get_model(mapping[module_name])


# TREND CALCULATOR
def calculate_trend(values):
    if not values or len(values) < 2:
        return "no_trend"

    if values[0] > values[-1]:
        return "increasing"
    elif values[0] < values[-1]:
        return "decreasing"
    return "stable"


# SUMMARY: HEALTH MODULES
def calculate_summary(module, records):

    recs = list(records)
    if not recs:
        return {"message": "No records found"}

    # HEIGHT
    if module == "height":
        values = [normalize_value(r.value, r.unit, "height") for r in recs]
        return {
            "latest_value": values[0],
            "unit": "cm",
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "average": round(mean(values), 2),
            "trend": calculate_trend(values)
        }

    # WEIGHT
    if module == "weight":
        values = [normalize_value(r.value, r.unit, "weight") for r in recs]
        return {
            "latest_value": values[0],
            "unit": "kg",
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "average": round(mean(values), 2),
            "trend": calculate_trend(values)
        }

    # BMI
    if module == "bmi":
        values = [r.value for r in recs]
        return {
            "latest_value": values[0],
            "category": bmi_category(values[0]),
            "min": min(values),
            "max": max(values),
            "average": round(mean(values), 2),
            "trend": calculate_trend(values)
        }

    # BLOOD PRESSURE
    if module == "blood_pressure":
        sys_vals = [r.systolic for r in recs]
        dia_vals = [r.diastolic for r in recs]
        return {
            "latest": {
                "systolic": sys_vals[0],
                "diastolic": dia_vals[0],
                "type": recs[0].type,
                "category": recs[0].category,
            },
            "min_systolic": min(sys_vals),
            "max_systolic": max(sys_vals),
            "min_diastolic": min(dia_vals),
            "max_diastolic": max(dia_vals),
            "trend_systolic": calculate_trend(sys_vals),
            "trend_diastolic": calculate_trend(dia_vals),
        }

    # HEART RATE
    if module == "heart_rate":
        values = [r.value for r in recs]
        return {
            "latest_value": values[0],
            "unit": "bpm",
            "min": min(values),
            "max": max(values),
            "average": round(mean(values), 2),
            "trend": calculate_trend(values),
        }

    # OXYGEN
    if module == "oxygen":
        values = [r.value for r in recs]
        return {
            "latest_value": values[0],
            "unit": "%",
            "min": min(values),
            "max": max(values),
            "average": round(mean(values), 2),
            "trend": calculate_trend(values),
        }

    # GLUCOSE
    if module == "glucose":
        values = [normalize_value(r.value, r.unit, "glucose") for r in recs]
        return {
            "latest_value": values[0],
            "unit": "mg/dl",
            "latest_type": recs[0].test_type,
            "min": min(values),
            "max": max(values),
            "average": round(mean(values), 2),
            "trend": calculate_trend(values)
        }

    # NON-NUMERIC MODULES WITH ADVANCED SUMMARIES
    if module == "prescriptions":
        return summarize_prescriptions(recs)

    if module == "hospitalizations":
        return summarize_hospitalizations(recs)

    if module == "medical_bills":
        return summarize_medical_bills(recs)

    if module == "vaccination_certificates":
        return summarize_vaccinations(recs)

    if module == "medicine_reminders":
        return summarize_medicine_reminders(recs)

    return {"message": "Unsupported module"}


# NON-NUMERIC SUMMARY FUNCTIONS
def summarize_prescriptions(recs):
    latest = recs[0]

    type_count = Counter([r.get_record_type_display() for r in recs])
    doctor_count = Counter([r.doctor_name for r in recs if r.doctor_name])

    return {
        "total_records": len(recs),
        "latest_record_type": latest.get_record_type_display(),
        "latest_record_date": latest.record_date,
        "top_prescription_type": type_count.most_common(1)[0][0],
        "top_doctor_visited": doctor_count.most_common(1)[0][0] if doctor_count else None,
        "records_by_type": type_count,
    }


def summarize_hospitalizations(recs):
    latest = recs[0]

    type_count = Counter([r.hospitalization_type for r in recs])
    hospital_count = Counter([r.hospital_name for r in recs])

    return {
        "total_hospitalizations": len(recs),
        "latest_admission": latest.admitted_date,
        "latest_discharge": latest.discharged_date,
        "common_hospital": hospital_count.most_common(1)[0][0],
        "records_by_type": type_count,
    }


def summarize_medical_bills(recs):
    latest = recs[0]

    hospital_count = Counter([r.record_hospital_name for r in recs])
    total_amount = sum([r.amount for r in recs if hasattr(r, "amount")])

    return {
        "total_bills": len(recs),
        "latest_bill_date": latest.record_date,
        "total_amount_spent": total_amount,
        "average_bill_amount": total_amount / len(recs) if recs else 0,
        "top_hospital": hospital_count.most_common(1)[0][0],
        "bills_by_hospital": hospital_count,
    }


def summarize_vaccinations(recs):
    latest = recs[0]

    dose_count = Counter([r.vaccination_name for r in recs])

    return {
        "total_vaccinations": len(recs),
        "latest_vaccination_name": latest.vaccination_name,
        "latest_vaccination_date": latest.vaccination_date,
        "vaccinations_by_type": dose_count,
    }


def summarize_medicine_reminders(recs):

    today = timezone.localdate()

    active_records = []
    completed_records = []

    for r in recs:
        record_data = {
            "id": r.id,
            "medicine_name": r.medicine_name,
            "start_date": r.start_date,
            "end_date": r.end_date,
            "frequency_type": r.frequency_type,
        }

        # Active: today is between start & end
        if r.start_date <= today <= r.end_date:

            # Add schedule times for fixed mode
            if r.frequency_type == "fixed_times":
                record_data["schedule_times"] = [
                    str(t.time)[:5] for t in r.schedule_times.all()
                ]

            active_records.append(record_data)

        # Completed: end_date is in the past
        elif r.end_date < today:
            completed_records.append(record_data)

        else:
            pass

    # Most frequent medicine
    medicine_count = Counter([r.medicine_name for r in recs])
    most_frequent = (
        medicine_count.most_common(1)[0][0] if medicine_count else None
    )

    return {
        "total_reminders": len(recs),
        "active_count": len(active_records),
        "completed_count": len(completed_records),
        "most_frequent_medicine": most_frequent,
        "active_reminders": active_records,
        "completed_reminders": completed_records,
    }

# BMI CATEGORY
def bmi_category(value):
    if value < 18.5:
        return "Underweight"
    elif value < 24.9:
        return "Normal"
    elif value < 29.9:
        return "Overweight"
    return "Obese"
