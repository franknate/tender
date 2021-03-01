from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.

class HomeView(LoginRequiredMixin, View):
    template = 'home.html'

    def get(self, request):
        return render(request, self.template)

class DisplayView(LoginRequiredMixin, View):
    template = 'display.html'

    def get(self, request):
        return render(request, self.template)
