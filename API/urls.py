from django.contrib import admin
from django.urls import path

from API import views


urlpatterns = [
    path('', views.index),
    path('user/me', views.selectMyself),

    path('signin', views.signin),
    path('signup', views.signup),
    path('patch-nickname', views.updateNickname),
    path('click/up', views.clickUp),
    path('time-challenge/record', views.clickTimeChallengeRecord),
    path('click/ranking/<int:number>', views.showClickRanking),
    path('time-challenge/ranking/<int:number>', views.showTimeChallengeRanking),
]
