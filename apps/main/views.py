from django.views import View
from django.shortcuts import render
from .forms import ProducerForm


# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html')


class ProducerView(View):
    def get(self, request):
        return render(request, 'producer.html', {
            'form': ProducerForm
        })
