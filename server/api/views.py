# from django.db.models.query_utils import Q
# from django.shortcuts import render
# from django.db.models import query
# from django.http import request
from django.views.decorators.csrf import requires_csrf_token
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import filters

from core.models import *
from .serializers import *

BASE_URL = 'http://188.93.211.127:8000'

class GetUserDataView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = UserSerializer(request.user).data
            data['current_reservation']['qr_image'] = BASE_URL + data['current_reservation']['qr_image']
            for i in data['favourites']:
                i['image'] = BASE_URL + i['image']

            return Response(data, status=status.HTTP_200_OK)
        except Exception: 
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class AddToFavouritesView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            wash = Wash.objects.get(pk=request.data['wash'])
            user = request.user
            if wash in user.favourites.all():
                user.favourites.remove(wash)
            else:
                user.favourites.add(wash)
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception: 
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetWashsView(generics.ListAPIView):
    queryset = Wash.objects.all()
    serializer_class = WashSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price_level', 'rating']
    filterset_fields = ['id', ]

    def get_queryset(self):
        queryset = Wash.objects.all()
        try:
            slot = Slot.objects.get(pk=self.request.GET['slot'])
            l = []
            for item in queryset:
                if slot in item.available_slots:
                    l.append(item.pk)
            queryset = Wash.objects.filter(id__in=l)
        except Exception:
            pass

        try:
            queryset = queryset.filter(services__type__pk=self.request.GET['service'])
        except Exception:
            pass

        return queryset


class CreateReservationView(generics.CreateAPIView):
    queryset = Reservation.objects.all().order_by('pk')
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]


class GetSlotsView(generics.ListAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [AllowAny]


class GetReviewsView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('-pk')
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['wash', ]


class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = CreateReviewSerializer
    permission_classes = [AllowAny]


class UpdateWashView(generics.UpdateAPIView):
    queryset = Wash.objects.all()
    serializer_class = WashSerializer
    permission_classes = [AllowAny]


class GetReservationsView(generics.ListAPIView):
    queryset = Reservation.objects.all().order_by('slot__pk')
    serializer_class = ReservationGetSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['wash', ]