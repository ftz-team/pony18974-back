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
]
