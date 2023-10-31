from django.urls import path

from .views import start_order

urlpatterns = [
    path('sart_order/', start_order, name='start_order'),
]