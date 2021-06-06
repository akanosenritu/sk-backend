from rest_framework import serializers

from api.models import *


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            "username",
            "is_staff"
        ]
    
    
class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = [
            "uuid",
            "text"
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "uuid",
            "last_name",
            "last_name_kana",
            "first_name",
            "first_name_kana"
        ]


class RegisteredStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredStaff
        fields = [
            "uuid",
            "staff_id",
            "gender",
            "last_name",
            "last_name_kana",
            "first_name",
            "first_name_kana",
            "birth_date",
            "registered_date",
            "is_active",
            "telephone_number",
            "email_address"
        ]


class ClothesSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesSetting
        fields = [
            "uuid",
            "title",
            "content"
        ]


class GatheringPlaceSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatheringPlaceSetting
        fields = [
            "uuid",
            "title",
            "content"
        ]


class PositionDataSerializer(serializers.ModelSerializer):
    clothes = ClothesSettingSerializer(read_only=True)
    clothes_uuid = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        queryset=ClothesSetting.objects.all(),
        source="clothes",
        write_only=True
    )
    gathering_place = GatheringPlaceSettingSerializer(read_only=True)
    gathering_place_uuid = serializers.PrimaryKeyRelatedField(
        allow_null=True,
        queryset=GatheringPlaceSetting.objects.all(),
        source="gathering_place",
        write_only=True,
    )
    
    def validate(self, data):
        for key in data.keys():
            if data[key] is None and data["nullable"] is False:
                raise serializers.ValidationError(
                    f"Field {key} is null. If field 'nullable' is set to False, all fields must not be null."
                )
        return data
    
    class Meta:
        model = PositionData
        fields = [
            "uuid",
            "start_hour",
            "end_hour",
            "male",
            "female",
            "unspecified",
            "clothes",
            "clothes_uuid",
            "gathering_place",
            "gathering_place_uuid",
            "nullable"
        ]


class PositionSerializer(serializers.ModelSerializer):
    data = PositionDataSerializer(read_only=True)
    data_uuid = serializers.PrimaryKeyRelatedField(
        queryset=PositionData.objects.all(),
        source="data",
        write_only=True
    )
    assigned_staffs = RegisteredStaffSerializer(many=True, read_only=True)
    assigned_staff_uuids = serializers.PrimaryKeyRelatedField(queryset=RegisteredStaff.objects.all(), many=True, source="assigned_staffs", write_only=True)
    
    class Meta:
        model = Position
        fields = [
            "uuid",
            "date",
            "data",
            "data_uuid",
            "assigned_staffs",
            "assigned_staff_uuids",
        ]


class PositionGroupSerializer(serializers.ModelSerializer):
    default_position_data = PositionDataSerializer(read_only=True)
    default_position_data_uuid = serializers.PrimaryKeyRelatedField(
        queryset=PositionData.objects.all(),
        source="default_position_data",
        write_only=True,
    )
    positions = PositionSerializer(read_only=True, many=True)
    position_uuids = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        source="positions",
        write_only=True,
        many=True
    )
    
    class Meta:
        model = PositionGroup
        fields = [
            "uuid",
            "title",
            "default_position_data",
            "default_position_data_uuid",
            "positions",
            "position_uuids",
            "position_color"
        ]


class EventSerializer(serializers.ModelSerializer):
    position_groups = PositionGroupSerializer(read_only=True, many=True)
    position_group_uuids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=PositionGroup.objects.all(),
        source="position_groups",
        write_only=True
    )
    
    class Meta:
        model = Event
        fields = [
            "uuid",
            "title",
            "datetime_added",
            "datetime_last_modified",
            "position_groups",
            "position_group_uuids"
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    staff = RegisteredStaffSerializer(read_only=True)
    staff_uuid = serializers.PrimaryKeyRelatedField(
        queryset=RegisteredStaff.objects.all(),
        source="staff",
        write_only=True
    )
    event = EventSerializer(read_only=True)
    event_uuid = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        source="event",
        write_only=True
    )
    
    class Meta:
        model = Application
        fields = [
            "uuid",
            "staff",
            "staff_uuid",
            "applied_at_date",
            "applied_to_date",
            "event",
            "event_uuid",
        ]
