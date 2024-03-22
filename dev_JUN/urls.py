from django.contrib import admin
from django.urls import path

from dev_JUN import views


urlpatterns = [
    path('', views.index),
    path('test/<int:user_id>', views.getUser),
    path('signin', views.signin),
    path('signup', views.signup),
    path('jwt', views.jwtTest),
]
