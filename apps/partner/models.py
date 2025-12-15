from django.db import models


class Partner(models.Model):
    name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
