from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import RoomSearchFilter
from .serializers import (
    RoomSerializer, BookCreateSerializer, BookViewSerializer
)
from booking.models import Room, BookingUser


class RoomViewSet(ReadOnlyModelViewSet):
    queryset = Room.objects.all()
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = RoomSearchFilter
    ordering_fileds = ('cost', 'population')
    serializer_class = RoomSerializer


class BookAPIView(APIView):
    def post(
        self, request: Request, room_id: int
    ) -> Response:
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        serializer = BookCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        get_object_or_404(Room, pk=room_id)
        bu_qs_bad = BookingUser.objects.filter(room_id=room_id).filter((
            Q(date_start__lte=data['date_start']) & Q(
                date_end__gt=data['date_start']
            )
        ) | (Q(date_start__lt=data['date_end']) & Q(
            date_end__gte=data['date_end']
        )) | (Q(date_start__gte=data['date_start']) & Q(date_end__lte=data[
            'date_end'
        ])))
        if bu_qs_bad.exists():
            return Response(
                'Room is not available for booking',
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            book = BookingUser.objects.create(
                user_id=request.user.id,
                room_id=room_id,
                date_start=data['date_start'],
                date_end=data['date_end']
            )
            serializer = BookViewSerializer(instance=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, room_id: int) -> Response:
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        get_object_or_404(Room, pk=room_id)
        bu_qs = BookingUser.objects.filter(
            room_id=room_id,
            user_id=request.user.id,
            date_start=data['date_start'],
            date_end=data['date_end']
        )
        if not bu_qs.exists():
            return Response(
                'Booking does not exist', status=status.HTTP_400_BAD_REQUEST
            )
        bu_qs.delete()
        return Response('Deleted', status=status.HTTP_204_NO_CONTENT)


class BookingViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookViewSerializer

    def get_queryset(self) -> QuerySet:
        return BookingUser.objects.filter(user=self.request.user).all()
