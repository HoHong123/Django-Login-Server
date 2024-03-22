from django.urls import path
from . import views

"""
@author : PKH
@date   : 2024.02.05
@update : 2024.02.15
"""
urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('login/fail/', views.loginFailView),
    path('login/success/', views.loginSuccessView),
    
    path('login/tablecheck/', views.loginSuccessView),
    
    path('logout/', views.logoutView, name='logout'),
    
    path('google/login/', views.googleLogin, name='google'),
    path('google/login/<str:param>/', views.googleLoginParam, name='google'),
    path('google/login/tablecheck/<str:param>', views.googleLoginTablecheck),
    
    path('accounts/google/login/callback/', views.googleCallback, name='google_callback'),
]
