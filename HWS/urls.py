from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ============================
    # Google authentication
    path('', include('dev_PKH.urls')),
    
    # ============================
    path('jun/', include('dev_JUN.urls')),

    # =======dev====== 
    path('api/', include(('API.urls'))),
]
