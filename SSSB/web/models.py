import json
from bson import ObjectId
from datetime import datetime, date, timedelta
import pytz
from django.db import models
from djongo import models as djongo_models

import sys
from pathlib import Path
app_dir = Path(__file__).parent.parent.parent
sys.path.append(app_dir.as_posix())

from send_mail import send_mail, build_message
from jinja2 import Environment, FileSystemLoader

# Create your models here.

def parse_datetime_with_24_hour(value):
    """
    Parses a datetime string, handling the special case where the time is '24:00:00'.
    
    Args:
        value (str): The datetime string in the format '%Y-%m-%d %H:%M:%S', 
                     e.g., '2024-11-18 24:00:00'.
    
    Returns:
        datetime: A datetime object representing the parsed datetime.
    """
    try:
        if "24:00:00" in value:
            # Split into date and time components
            date_part, _ = value.split(' ')
            # Replace '24:00:00' with '00:00:00' and add one day
            value = f"{date_part} 00:00:00"
            naive_datetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S') + timedelta(days=1)
        else:
            # Parse normally if no '24:00:00' is found
            naive_datetime = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return naive_datetime
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {value}") from e

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

class StringDateField(models.DateTimeField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD'.")
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, datetime):
            return value.date().strftime('%Y-%m-%d')
        if isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        return super().get_prep_value(value)


class StringDateTimeField(models.DateTimeField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                naive_datetime = parse_datetime_with_24_hour(value)
                stockholm_tz = pytz.timezone("Europe/Stockholm")
                localized_datetime = stockholm_tz.localize(naive_datetime)
                return localized_datetime
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD HH:MM:SS'.")
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                naive_datetime = parse_datetime_with_24_hour(value)
                stockholm_tz = pytz.timezone("Europe/Stockholm")
                localized_datetime = stockholm_tz.localize(naive_datetime)
                return localized_datetime
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD HH:MM:SS'.")
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return super().get_prep_value(value)


class StringDateTimeFieldUTC(models.DateTimeField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                naive_datetime = parse_datetime_with_24_hour(value)
                localized_datetime = pytz.utc.localize(naive_datetime)
                return localized_datetime
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD HH:MM:SS'.")
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                naive_datetime = parse_datetime_with_24_hour(value)
                localized_datetime = pytz.utc.localize(naive_datetime)
                return localized_datetime
            except ValueError:
                raise ValueError("Invalid date format. Expected 'YYYY-MM-DD HH:MM:SS'.")
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        return super().get_prep_value(value)

class JSONField(models.JSONField):
    def from_db_value(self, value, expression, connection):
        if isinstance(value, str):
            return json.loads(value)
        return value

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except ValueError:
                raise ValueError("Invalid JSON format.")
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, dict) or isinstance(value, list):
            return value
        return super().get_prep_value(value)


#class FloorField(models.IntegerField):
#    def from_db_value(self, value, expression, connection):
#        if value is None:
#            return value
#        if isinstance(value, str):
#            if value.upper() == "SU":
#                return -1
#            elif value.upper() == "GF":
#                return 0
#            else:
#                try:
#                    return int(value)
#                except ValueError:
#                    raise ValueError(f"Invalid floor value {value}. Expected 'SU', 'GF' or an integer.")
#        return value
#
#    def to_python(self, value):
#        if value is None:
#            return value
#        if isinstance(value, str):
#            if value.upper() == "SU":
#                return -1
#            elif value.upper() == "GF":
#                return 0
#            else:
#                try:
#                    return int(value)
#                except ValueError:
#                    raise ValueError(f"Invalid floor value {value}. Expected 'SU', 'GF' or an integer.")
#        return value
#
#    def get_prep_value(self, value):
#        if value is None:
#            return value
#        if isinstance(value, int):
#            if value == -1:
#                return "SU"
#            elif value == 0:
#                return "GF"
#            return str(value)
#        return super().get_prep_value(value)
#
#    def get_db_prep_value(self, value, connection, prepared=False):
#        """
#        This method ensures that the value is correctly prepared for database queries,
#        such as when using `__gte`, `__lte`, etc.
#        """
#        if value is None:
#            return value
#        if isinstance(value, str):
#            if value.upper() == "SU":
#                return -1
#            elif value.upper() == "GF":
#                return 0
#            else:
#                try:
#                    return int(value)
#                except ValueError:
#                    raise ValueError("Invalid floor value. Expected 'SU', 'GF' or an integer.")
#        elif isinstance(value, int):
#            return value
#        return super().get_db_prep_value(value, connection, prepared)
#
#    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
#        """
#        Handle lookups such as __gte and __lte.
#        """
#        if lookup_type in ['gte', 'lte', 'exact', 'gt', 'lt']:
#            value = self.get_db_prep_value(value, connection, prepared)
#        return super().get_db_prep_lookup(lookup_type, value, connection, prepared)

class ApartmentAmount(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    update_time = StringDateTimeFieldUTC(null=True, blank=True, default=None)
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
    update_time = StringDateTimeFieldUTC(null=True, blank=True, auto_now=True)
    name = models.CharField(max_length=255, null=True, blank=True, default=None)
    object_number = models.CharField(max_length=255, null=True, blank=True, default=None)
    url = models.URLField(null=True, blank=True, default=None)
    housing_area = models.CharField(max_length=255, null=True, blank=True, default=None)
    address = models.CharField(max_length=255, null=True, blank=True, default=None)
    accommodation_type = models.CharField(max_length=255, null=True, blank=True, default=None)
    floor = models.IntegerField(null=True, blank=True, default=None)
    living_space = models.IntegerField(null=True, blank=True, default=None)
    monthly_rent = models.IntegerField(null=True, blank=True, default=None)
    valid_from = StringDateField(null=True, blank=True, default=None)
    end_date = StringDateField(null=True, blank=True, default=None)
    floor_drawing = models.CharField(max_length=255, null=True, blank=True, default=None)
    apartment_drawing = models.CharField(max_length=255, null=True, blank=True, default=None)
    application_ddl = StringDateTimeField(null=True, blank=True, default=None)
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
        blank=True,
        default=None
    )

    class Meta:
        managed = True
        db_table = 'apartment_info'

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = ObjectId()
        super().save(*args, **kwargs)

class ApartmentStatus(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    update_time = StringDateTimeFieldUTC(null=True, blank=True, default=None)
    object_number = models.CharField(max_length=255, null=True, blank=True, default=None)
    queue_len = models.IntegerField(null=True, blank=True, default=None)
    most_credit = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        managed = True
        db_table = 'apartment_status'

    def save(self, *args, **kwargs):
        if self._id is None:
            self._id = ObjectId()
        super().save(*args, **kwargs)


class PersonalFilter(models.Model):
    _id = ObjectIdField(primary_key=True, default=None)
    update_time = StringDateTimeFieldUTC(null=True, blank=True, auto_now=True)

    email = models.EmailField(max_length=255)
    regions = JSONField(null=True, blank=True, default=None)
    types = JSONField(null=True, blank=True, default=None)
    address = models.CharField(max_length=255, null=True, blank=True, default=None)
    
    # [min, max] fields
    living_space = JSONField(null=True, blank=True, default=None)
    rent = JSONField(null=True, blank=True, default=None)
    floor = JSONField(null=True, blank=True, default=None)

    short_rent = models.BooleanField(null=True, blank=True, default=False) 
    electricity_include = models.BooleanField(null=True, blank=True, default=False)
    rent_free_june_and_july = models.BooleanField(null=True, blank=True, default=False)
    max_4_years = models.BooleanField(null=True, blank=True, default=False)
    current_credit = models.IntegerField(default=100000) 
    credit_start = StringDateField(null=True, blank=True, default=None)
    active = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'personal_filter'

    def get_credit_start(self, credit):
        credit = int(credit)
        sweden_timezone = pytz.timezone('Europe/Stockholm')
        now_time = sweden_timezone.normalize(datetime.now().astimezone(tz=sweden_timezone))
        start_time = now_time - timedelta(days=credit)
        return start_time

    def send_init_mail(self):
        receivers = [self.email]
        link = "https://sssbreminder.xyzs.app/?filter_id={}".format(self._id)

        curr_path = Path(__file__).resolve().parent
        env = Environment(loader=FileSystemLoader(app_dir / 'SSSB/templates'))
        template = env.get_template('initial_mail.html')  

        data = {
            "regions": ", ".join(self.regions) if len(self.regions) > 0 else "Not Specified",
            "types": ", ".join(self.types) if len(self.types) > 0 else "Not Specified",
            "address": self.address if self.address is not None and type(self.address) is str and self.address.strip() != "" else "Not Specified",
            "space": f"{self.living_space['min']} ~ {self.living_space['max']} m²" if self.living_space is not None else "Not Specified",
            "rent": f"{self.rent['min']} ~ {self.rent['max']} SEK" if self.rent is not None else "Not Specified",
            "floor": f"{self.floor['min']} ~ {self.floor['max']}" if self.floor is not None else "Not Specified",
            "current_credit": f"{self.current_credit} days" if self.current_credit is not None else "Not Specified",
            "credit_start": f"{self.credit_start.strftime('%Y-%m-%d')}" if self.credit_start is not None else "Not Specified",
            "electricity_include": "Yes" if self.electricity_include else "No" if self.electricity_include is not None else "Not Specified",
            "rent_free_june_and_july": "Yes" if self.rent_free_june_and_july else "No" if self.rent_free_june_and_july is not None else "Not Specified",
            "max_4_years": "Yes" if self.max_4_years else "No" if self.max_4_years is not None else "Not Specified",
            "short_rent": "Yes" if self.short_rent else "No" if self.short_rent is not None else "Not Specified",
            "modify_url": link,
        }

        msg = build_message(receivers, 
                            title="SSSB Reminder created successfully",
                            content=template.render(**data))
        send_mail(receivers, msg)

    def save(self, *args, **kwargs):
        if self.credit_start is None:
            self.credit_start = self.get_credit_start(self.current_credit)
        if self._id is None:
            self._id = ObjectId()
            self.send_init_mail()
        super().save(*args, **kwargs)


