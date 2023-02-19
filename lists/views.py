from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    if request.method == 'POST':
        context = {
            'new_item_text': request.POST['item_text']
        }
        return render(request=request, template_name='lists/home.html', context=context)

    return render(request=request, template_name='lists/home.html')


