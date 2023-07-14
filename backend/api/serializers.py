from collections import OrderedDict

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList

from booking.models import Room, BookingUser


class BookViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingUser
        fields = ('user_id', 'room_id', 'date_start', 'date_end')


class BookShortViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingUser
        fields = ('user_id', 'date_start', 'date_end')


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ('id', 'number_or_title', 'cost', 'population', 'users')

    def get_id(self, obj: Room) -> int:
        return obj.pk

    def get_users(self, obj: Room) -> ReturnList:
        bu = BookingUser.objects.filter(room=obj)
        return BookShortViewSerializer(bu, many=True).data


class BookCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookingUser
        fields = ('date_start', 'date_end')

    def validate(self, data: OrderedDict) -> OrderedDict:
        if data['date_start'] > data['date_end']:
            raise serializers.ValidationError(
                "Start date must be before end date"
            )
        return data
