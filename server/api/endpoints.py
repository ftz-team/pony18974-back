from django.urls import path, include
from django.conf.urls import url
from rest_framework.generics import CreateAPIView, DestroyAPIView
from .views import *

api_urls = [
    url(r'^rest-auth/', include('rest_auth.urls')),

    path('user/get/', GetUserDataView.as_view(), name='get_user_data'),
    path('add_to_fav/', AddToFavouritesView.as_view(), name='add_to_fav'),

    path('wash/list/', GetWashsView.as_view(), name='wash_list'),
    path('create_reservation/', CreateReservationView.as_view(), name='create_reservation'),

    path('get_slots/', GetSlotsView.as_view(), name='get_slots'),

    path('create_review/', CreateReviewView.as_view(), name='create_review'),
    path('get_reviews/', GetReviewsView.as_view(), name='get_reviews'),
    path('get_reservations/', GetReservationsView.as_view(), name='get_reservations'),
    path('upd_wash/<pk>/', UpdateWashView.as_view(), name='upd_wash'),
]
