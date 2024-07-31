from rest_framework import serializers
from .models import ApartmentAmount

class ApartmentAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAmount
        fields = '__all__'
