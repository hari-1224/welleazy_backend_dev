# create centers
from apps.gym_service.models import GymCenter, GymPackage
GymCenter.objects.create(
    name="Cult Indiranagar",
    type="GX",
    business_line="ELITE",
    address="1st floor, Above Ritu Kumar, Indiranagar Double Rd, HAL 2nd Stage, Indiranagar, Bengaluru",
    city="Bengaluru",
    state="Karnataka",
)

# packages
GymPackage.objects.create(title="3 MONTHS", duration_months=3, original_price=9092, discounted_price=7728, discount_percent=15, features=[
    "Access to cult centres",
    "Access to cult gyms",
    "Access to all centers",
    "Access to cult home",
    "45 days membership pause",
])
GymPackage.objects.create(title="6 MONTHS", duration_months=6, original_price=12732, discounted_price=10186, discount_percent=20, features=[...])
GymPackage.objects.create(title="12 MONTHS", duration_months=12, original_price=15525, discounted_price=11644, discount_percent=25, features=[...])
