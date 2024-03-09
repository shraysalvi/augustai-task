from rest_framework import serializers
from .models import Notification
from django.contrib.auth.models import User
from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask, SolarSchedule, ClockedSchedule, crontab_schedule_celery_timezone
from drf_writable_nested import WritableNestedModelSerializer
import json


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class IntervalScheduleSerializer(serializers.ModelSerializer):
    required = False

    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class SolarScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarSchedule
        fields = '__all__'


class ClockedScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockedSchedule
        fields = '__all__'


class CrontabSerializer(serializers.ModelSerializer):
    timezone = serializers.CharField(default=crontab_schedule_celery_timezone)
    minute = serializers.CharField(default='0')
    hour = serializers.CharField(default='0')
    day_of_month = serializers.CharField(default='*')
    month_of_year = serializers.CharField(default='*')
    day_of_week = serializers.CharField(default='*')

    class Meta:
        model = CrontabSchedule
        fields = '__all__'


class PeriodicTaskSerializer(serializers.ModelSerializer):
    # interval = IntervalScheduleSerializer(required=False)
    crontab = CrontabSerializer()
    # solar = SolarScheduleSerializer(required=False)
    # clocked = ClockedScheduleSerializer(required=False)
    task = serializers.CharField(
        read_only=True, default='Send Email Notification')

    class Meta:
        model = PeriodicTask
        fields = ["name", "kwargs", "task", "crontab", "expires", "expire_seconds", "one_off",
                  "start_time", "enabled", "last_run_at", "total_run_count", "date_changed", "description"]

    def validate_kwargs(self, value):
        if not value:
            raise serializers.ValidationError(
                "kwargs cannot be empty. Include `emails`, `subject` and `body` as JSON string.")
        try:
            kwargs_dict = json.loads(value)
        except json.JSONDecodeError:
            raise serializers.ValidationError(
                "kwargs must be a valid JSON string")

        if 'emails' not in kwargs_dict:
            raise serializers.ValidationError(
                "kwargs must contain 'emails' as list of emails")
        if 'subject' not in kwargs_dict:
            raise serializers.ValidationError(
                "kwargs must contain 'subject' as text")
        if 'body' not in kwargs_dict:
            raise serializers.ValidationError(
                "kwargs must contain 'body' as text")
        if not isinstance(kwargs_dict['emails'], list):
            raise serializers.ValidationError(
                "emails should be list string of emails")

        return value

    def create(self, validated_data):
        # interval = validated_data.pop('interval', None)
        # solar = validated_data.pop('solar', None)
        # clocked = validated_data.pop('clocked', None)

        # if interval:
        #     interval_schedule = IntervalSchedule.objects.create(**interval)
        #     validated_data['interval'] = interval_schedule

        # if solar:
        #     solar_schedule = SolarSchedule.objects.create(**solar)
        #     validated_data['solar'] = solar_schedule

        # if clocked:
        #     clocked_schedule = ClockedSchedule.objects.create(**clocked)
        #     validated_data['clocked'] = clocked_schedule

        crontab = validated_data.pop('crontab')
        crontab_schedule, created = CrontabSchedule.objects.get_or_create(
            **crontab)
        validated_data['crontab'] = crontab_schedule
        return super().create(validated_data)


class NotificationSerializer(WritableNestedModelSerializer):
    user = UserSerializer(
        read_only=True, default=serializers.CurrentUserDefault())
    tasks = PeriodicTaskSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'tasks']
