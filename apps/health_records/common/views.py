from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.apps import apps

# Import serializers
from apps.health_records.prescriptions.serializers import PrescriptionRecordSerializer
from apps.health_records.hospitalizations.serializers import HospitalizationRecordSerializer
from apps.health_records.medical_bills.serializers import MedicalBillRecordSerializer
from apps.health_records.vaccination_certificates.serializers import VaccinationCertificateRecordSerializer


MODULE_CONFIG = {
    "prescriptions": {
        "model": "prescriptions.PrescriptionRecord",
        "serializer": PrescriptionRecordSerializer,
        "doctor_field": "doctor_name",
        "hospital_field": None
    },
    "hospitalizations": {
        "model": "hospitalizations.HospitalizationRecord",
        "serializer": HospitalizationRecordSerializer,
        "doctor_field": "doctor_name",
        "hospital_field": "hospital_name"
    },
    "medical_bills": {
        "model": "medical_bills.MedicalBillRecord",
        "serializer": MedicalBillRecordSerializer,
        "doctor_field": None,
        "hospital_field": "record_hospital_name"
    },
    "vaccination_certificates": {
        "model": "vaccination_certificates.VaccinationCertificateRecord",
        "serializer": VaccinationCertificateRecordSerializer,
        "doctor_field": None,
        "hospital_field": "vaccination_center"
    },
}


def apply_common_filters(qs, params, doctor_field, hospital_field):

    # text search
    if params.get("search_text"):
        text = params["search_text"]
        query = Q()

        if doctor_field:
            query |= Q(**{f"{doctor_field}__icontains": text})

        if hospital_field:
            query |= Q(**{f"{hospital_field}__icontains": text})

        qs = qs.filter(query)

    # date filter
    if params.get("start_date"):
        qs = qs.filter(created_at__date__gte=params["start_date"])

    if params.get("end_date"):
        qs = qs.filter(created_at__date__lte=params["end_date"])

    # self/dependant/both
    sd = params.get("self_or_dependant")
    if sd == "self":
        qs = qs.filter(for_whom="self")
    elif sd == "dependant":
        qs = qs.filter(for_whom="dependant")

    # specific dependant
    if params.get("dependant_id"):
        qs = qs.filter(dependant_id=params["dependant_id"])

    return qs


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def search_records(request):

    module = request.data.get("module", "all")
    params = request.data

    results = {}

    # Search in all modules
    modules_to_search = (
        MODULE_CONFIG.keys() if module == "all" else [module]
    )

    for mod in modules_to_search:

        if mod not in MODULE_CONFIG:
            return Response({"error": f"Invalid module: {mod}"}, status=400)

        cfg = MODULE_CONFIG[mod]
        model = apps.get_model(cfg["model"])
        serializer = cfg["serializer"]

        qs = model.objects.filter(
            user=request.user,
            deleted_at__isnull=True
        )

        qs = apply_common_filters(
            qs,
            params,
            cfg["doctor_field"],
            cfg["hospital_field"]
        )

        results[mod] = serializer(qs, many=True).data

    return Response({
        "search_filters": params,
        "results": results
    })
