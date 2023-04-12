from django.urls import path
from api import views

urlpatterns = [
    path('facelogin/',views.facelogin,name='facelogin'),
]
