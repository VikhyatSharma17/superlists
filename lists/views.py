from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item, List

def home_page(request):
    return render(request=request, template_name='lists/home.html')

def view_list(request, list_id):
    list_to_view = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_to_view)
    context = {
        'items': items,
        'list': list_to_view,
    }

    return render(request=request, template_name='lists/list.html', context=context)

def new_list(request):
    created_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=created_list)
    return redirect(f'/lists/{created_list.id}/')

def add_item(request, list_id):
    list_to_use = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_to_use)
    context = {
        'items': Item.objects.filter(list=list_to_use)
    }

    return redirect(f'/lists/{list_to_use.id}/')

