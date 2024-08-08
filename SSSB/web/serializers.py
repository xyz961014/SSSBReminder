from rest_framework import serializers
from .models import Bid
from .models import ApartmentAmount, ApartmentInfo, ApartmentStatus

class ApartmentAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAmount
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ["queue_len", "most_credit"]

class ApartmentInfoSerializer(serializers.ModelSerializer):
    bid = BidSerializer()

    class Meta:
        model = ApartmentInfo
        fields = '__all__'

class ApartmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentStatus
        fields = '__all__'
