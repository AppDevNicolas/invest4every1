from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_page),
    #path('test/', views.test_page, name='test_page'),
]
