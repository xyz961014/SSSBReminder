from django.db import models
from bson import ObjectId
from djongo import models as djongo_models

# Create your models here.

class ObjectIdField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 24
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return value
        return str(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return str(value)

    def get_prep_value(self, value):
        if value is None or value == '':
            return ObjectId()
        return ObjectId(value)


class ApartmentAmount(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    update_time = models.DateTimeField(null=True, blank=True, default=None)
    amount = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        managed = True
        db_table = 'apartment_amount'

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = ObjectId()
        super().save(*args, **kwargs)

class Bid(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    queue_len = models.IntegerField(null=True, blank=True, default=None)
    most_credit = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        managed = False

class Transit(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    from_location = models.CharField(max_length=100, null=True)
    to_location = models.CharField(max_length=100, null=True)
    mode = models.CharField(max_length=50, null=True)
    time = models.CharField(max_length=50, null=True)
    distance = models.FloatField(null=True)

    class Meta:
        managed = False

class Cycling(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    from_location = models.CharField(max_length=100, null=True)
    to_location = models.CharField(max_length=100, null=True)
    mode = models.CharField(max_length=50, null=True)
    time = models.CharField(max_length=50, null=True)
    distance = models.FloatField(null=True)

    class Meta:
        managed = False

class Distances(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    transit = djongo_models.EmbeddedField(
        model_container=Transit,
        null=True,
        blank=True
    )
    cycling = djongo_models.EmbeddedField(
        model_container=Cycling,
        null=True,
        blank=True
    )

    class Meta:
        managed = False

class ApartmentInfo(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    update_time = models.DateTimeField(null=True, blank=True, default=None)
    name = models.CharField(max_length=255, null=True, blank=True, default=None)
    object_number = models.CharField(max_length=255, null=True, blank=True, default=None)
    url = models.URLField()
    housing_area = models.CharField(max_length=255, null=True, blank=True, default=None)
    address = models.CharField(max_length=255, null=True, blank=True, default=None)
    accommodation_type = models.CharField(max_length=255, null=True, blank=True, default=None)
    floor = models.IntegerField(null=True, blank=True, default=None)
    living_space = models.IntegerField(null=True, blank=True, default=None)
    monthly_rent = models.IntegerField(null=True, blank=True, default=None)
    valid_from = models.DateField(null=True, blank=True, default=None)
    end_date = models.DateField(null=True, blank=True, default=None)
    floor_drawing = models.CharField(max_length=255, null=True, blank=True, default=None)
    apartment_drawing = models.CharField(max_length=255, null=True, blank=True, default=None)
    application_ddl = models.DateTimeField(null=True, blank=True, default=None)
    electricity_include = models.BooleanField(null=True, blank=True, default=None)
    rent_free_june_and_july = models.BooleanField(null=True, blank=True, default=None)
    max_4_years = models.BooleanField(null=True, blank=True, default=None)
    #distances = models.JSONField(null=True, blank=True)
    #distances = djongo_models.EmbeddedField(
    #    model_container=Distances,
    #    null=True,
    #    blank=True
    #)
    bid = djongo_models.EmbeddedField(
        model_container=Bid,
        null=True,
        blank=True
    )

    class Meta:
        managed = True
        db_table = 'apartment_info'

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = ObjectId()
        super().save(*args, **kwargs)
