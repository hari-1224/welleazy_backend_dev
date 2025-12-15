from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import SiteFeedback
from .serializers import SiteFeedbackSerializer
from apps.common.mixins.save_user_mixin import SaveUserMixin


class SiteFeedbackViewSet(SaveUserMixin, viewsets.ModelViewSet):
    queryset = SiteFeedback.objects.filter(deleted_at__isnull=True)
    serializer_class = SiteFeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    # CREATE FEEDBACK
    def create(self, request, *args, **kwargs):
        serializer = SiteFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        feedback = serializer.save(
            user=request.user,
            created_by=request.user,
            updated_by=request.user
        )

        return Response(
            {"message": "Feeedback submitted successfully", "data": SiteFeedbackSerializer(feedback).data},
            status=status.HTTP_201_CREATED
        )
