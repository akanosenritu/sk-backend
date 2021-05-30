import datetime
import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class MyUser(AbstractUser):
    pass


class Gender(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    text = models.CharField(max_length=10)


class Employee(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    last_name = models.CharField(max_length=30)
    last_name_kana = models.CharField(max_length=60)
    first_name = models.CharField(max_length=30)
    first_name_kana = models.CharField(max_length=60)
    

class RegisteredStaff(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    staff_id = models.IntegerField()
    
    gender = models.CharField(max_length=20, choices=(
        ("male", "男"),
        ("female", "女"),
        ("unspecified", "未指定")
    ))
    last_name = models.CharField(max_length=30)
    last_name_kana = models.CharField(max_length=60)
    first_name = models.CharField(max_length=30)
    first_name_kana = models.CharField(max_length=60)
    birth_date = models.DateField()
    
    registered_date = models.DateField(default=datetime.date.today)
    interviewed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    
    telephone_number = models.CharField(max_length=30)
    email_address = models.CharField(max_length=250)


class ClothesSetting(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    
    
class GatheringPlaceSetting(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    

class PositionData(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    start_hour = models.CharField(max_length=5, null=True, blank=True)
    end_hour = models.CharField(max_length=5, null=True, blank=True)
    male = models.IntegerField(null=True, blank=True)
    female = models.IntegerField(blank=True, null=True)
    unspecified = models.IntegerField(blank=True, null=True)
    clothes = models.ForeignKey(ClothesSetting, on_delete=models.SET_NULL, null=True, blank=True)
    gathering_place = models.ForeignKey(GatheringPlaceSetting, on_delete=models.SET_NULL, null=True, blank=True)
    
    # if nullable == False, all the other fields should not be null.
    # This is checked by the serializer on data submission.
    nullable = models.BooleanField()
    

class Position(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    date = models.DateField()
    data = models.ForeignKey(PositionData, on_delete=models.PROTECT)
    assigned_staffs = models.ManyToManyField(RegisteredStaff, related_name="position")


class PositionGroup(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    
    title = models.CharField(max_length=250)
    default_position_data = models.ForeignKey(PositionData, on_delete=models.PROTECT)
    positions = models.ManyToManyField(Position, related_name="position_group")
    position_color = models.CharField(max_length=10)


class Event(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_modified = models.DateTimeField(default=timezone.now)
    
    title = models.CharField(max_length=250)
    #  person_assigned_to = models.CharField(max_length=250)
    
    position_groups = models.ManyToManyField(PositionGroup, related_name="event")