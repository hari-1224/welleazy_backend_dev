
from rest_framework import serializers
from .models import CartItem,Cart,Prescription
from apps.addresses.serializers import AddressSerializer
from apps.pharmacy.cart.utils import estimate_delivery_date



class CartItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)
    image = serializers.ImageField(source="medicine.image", read_only=True)
    selling_price = serializers.DecimalField(source="medicine.selling_price", read_only=True, max_digits=10, decimal_places=2)
    mrp_price = serializers.DecimalField(source="medicine.mrp_price", read_only=True, max_digits=10, decimal_places=2)
    vendor_name=serializers.CharField(source="medicine.vendor.name", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "medicine", "medicine_name", "image", "selling_price", "mrp_price", "quantity","vendor_name",]



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    address=AddressSerializer(read_only=True)
    total_mrp = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_selling = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_on_mrp = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    handling_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    platform_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    delivery_charge = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    coupon_discount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_pay = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    applied_coupon = serializers.CharField(source="coupon.code", read_only=True)
    delivery_date = serializers.SerializerMethodField()
    delivery_mode=serializers.CharField()

    def get_delivery_date(self, obj):
        if obj.address:
            pincode = obj.address.pincode
            delivery = estimate_delivery_date(pincode)
            return delivery.strftime("%A, %d %B %Y")
        return None
    class Meta:
        model = Cart
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"


def get_download_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(
            f"/api/pharmacy/prescription/download/{obj.id}/"
        )