from rest_framework import serializers
from .models import Bid
from .models import ApartmentAmount, ApartmentInfo, ApartmentStatus, PersonalFilter

class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        return data 

    def to_representation(self, value):
        if isinstance(value, str):
            return json.loads(value)
        return value

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

class PersonalFilterSerializer(serializers.ModelSerializer):
    regions = JSONSerializerField()
    types = JSONSerializerField()
    living_space = JSONSerializerField(allow_null=True)
    rent = JSONSerializerField(allow_null=True)
    floor = JSONSerializerField(allow_null=True)

    class Meta:
        model = PersonalFilter
        fields = '__all__'
