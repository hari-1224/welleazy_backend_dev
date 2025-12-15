from django.apps import AppConfig


class PrescriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.health_records.prescriptions'
    label = 'prescriptions'
    