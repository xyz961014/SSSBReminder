from rest_framework import serializers
from .models import ApartmentAmount, ApartmentInfo

class ApartmentAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAmount
        fields = '__all__'

class ApartmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentInfo
        fields = '__all__'
