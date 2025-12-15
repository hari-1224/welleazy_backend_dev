from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import GymCenter, GymPackage, Voucher
from apps.dependants.models import Dependant

@admin.register(GymCenter)
class GymCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state')


@admin.register(GymPackage)
class GymPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration_months', 'original_price', 'discounted_price')


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id', 'voucher_uuid', 'user', 'package', 'gym_center', 'status', 'created_at')
    readonly_fields = ('voucher_uuid', 'created_at')


@admin.register(Dependant)
class DependantAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'user')
