from django.urls import path
from . import views

urlpatterns = [
    path('',views.RateView.as_view())
]