from django.apps import AppConfig


class VaccinationCertificatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.health_records.vaccination_certificates'
    label = 'vaccination_certificates'