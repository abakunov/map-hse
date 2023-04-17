from django.urls import path, include
from rest_framework.generics import CreateAPIView
from .views import *


api_urls = [
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('update-user/<int:pk>', UpdateUserView.as_view(), name='update-user'),
    path('get-users/', GetUsersView.as_view(), name='get-users'),
    path('get-user/<int:pk>', GetUserView.as_view(), name='get-user'),

    path('set-location/', SetLocationView.as_view(), name='set-location'),
    path('get-floors/', GetFloorsView.as_view(), name='get-floors'),

    path('get-interests/', GetInterestsView.as_view(), name='get-interests'),
    path('create-interest/', CreateInterestView.as_view(), name='create-interest'),

    path('set-view/', SetView.as_view(), name='set-view'),

    path('get-map/', MapView.as_view(), name='get-map'),
    path('get-in-coworking/', InCoworkingView.as_view(), name='get-in-coworking'),
    path('get-all-users/', GetAllUsersView.as_view(), name='get-all-users'),

    path('skip-user/', SkipUserView.as_view(), name='skip-user'),
    path('get-user-by-tg-id/', GetUserByTgIdView.as_view(), name='get-user-by_tg_id'),
]