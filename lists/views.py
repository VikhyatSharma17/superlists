from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item, List

def home_page(request):
    return render(request=request, template_name='lists/home.html')

def view_list(request):
    items = Item.objects.all()
    context = {
        'items': items
    }

    return render(request=request, template_name='lists/list.html', context=context)

def new_list(request):
    created_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=created_list)
    return redirect('/lists/the-only-list-in-the-world/')

