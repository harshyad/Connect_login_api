from django.urls import path
from api import views


urlpatterns = [
    path('facelogin',views.facelogin,name='facelogin'),
    path('login',views.login,name='login'),
    path('register',views.Register,name='regsiter'),
    path('update',views.update,name='update'),
    path('view',views.view,name='view')
]