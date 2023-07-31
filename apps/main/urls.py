from django.urls import path

from .views import HomeView, ProducerView, ConsumerView, SuccessView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('producer/', ProducerView.as_view(), name='producer'),
    path('consumer/', ConsumerView.as_view(), name='consumer'),
    path('success/', SuccessView.as_view(), name='success'),
]
