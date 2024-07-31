from django.db import models
from bson import ObjectId

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
    update_time = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        managed = True
        db_table = 'apartment_amount'

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = ObjectId()
        super().save(*args, **kwargs)


