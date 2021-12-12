from django.db.models import fields
from rest_framework import serializers

from core.models import *


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['pk', ]


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    type_name = serializers.ReadOnlyField()
    class Meta:
        model = Service
        fields = ['pk', 'type_name', 'price']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class WashSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True)
    pk_available_slots = serializers.ReadOnlyField()
    class Meta:
        model = Wash
        fields = '__all__'


class CreateWashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wash
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    current_reservation = ReservationSerializer()
    favourites = WashSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'


class UserGgSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'name', 'phone_number']


class ReservationGetSerializer(serializers.ModelSerializer):
    user = UserGgSerializer()
    class Meta:
        model = Reservation
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserGgSerializer()
    class Meta:
        model = Review
        fields = '__all__'