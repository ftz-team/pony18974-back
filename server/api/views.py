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


class GetUserDataView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            data = UserSerializer(request.user).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception: 
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class AddToFavouritesView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            wash = Wash.objects.get(pk=request.data['wash'])
            user = request.user
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
            queryset = queryset.filter(services__pk=self.request.GET['service'])
        except Exception:
            pass

        return queryset


class CreateReservationView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [AllowAny]


class GetSlotsView(generics.ListAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [AllowAny]