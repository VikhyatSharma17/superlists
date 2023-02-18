from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request=request, template_name='home.html')


