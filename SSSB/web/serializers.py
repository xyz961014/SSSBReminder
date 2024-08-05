from rest_framework import serializers
from .models import Bid
from .models import ApartmentAmount, ApartmentInfo

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
