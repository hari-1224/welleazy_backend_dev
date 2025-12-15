from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .summary_engine import get_model_from_module, calculate_summary


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def health_summary(request):
    module = request.data.get("module")

    if not module:
        raise ValidationError({"module": "module is required"})

    Model = get_model_from_module(module)

    qs = Model.objects.filter(user=request.user)
    if hasattr(Model, "deleted_at"):
        qs = qs.filter(deleted_at__isnull=True)

    qs = qs.order_by("-created_at")

    summary = calculate_summary(module, qs)

    return Response({
        "module": module,
        "summary": summary
    })
