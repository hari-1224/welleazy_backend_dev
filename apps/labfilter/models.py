from django.db import models
from apps.common.models import BaseModel

class VisitType(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
