"""
URL configuration for parking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from parkingApp.views import user_CRUD,userLoginApi,alluser,list_all_available_garage,reserve_spot,reservation_close
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api_auth/',include('rest_framework.urls')),
    path('api-user/',user_CRUD.as_view()),
    path('user-login/',userLoginApi.as_view()),
    path('all-user/',alluser.as_view()),

    path('garage/<int:id>/',list_all_available_garage.as_view()),

    path('reservespot/<int:spot_id>/',reserve_spot.as_view()),

    path('close/<int:reserve_id>/',reservation_close.as_view()),



]
