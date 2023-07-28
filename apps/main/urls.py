from django.urls import path

from .views import HomeView, ProducerView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('producer/', ProducerView.as_view(), name='producer'),
]
