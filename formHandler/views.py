from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FormModel, SubmitModel
import json
# Create your views here.
@csrf_exempt
def handle_form_submition_view(request, uid):
    if request.method=="POST":
        try:
            form = FormModel.objects.get(slug=uid)
        except:
            return JsonResponse({'status':'error', 'code': 'requested form not found'})
        data = {}
        for key, value in request.POST.items():
            data[key]=value
        
        newSubmit = SubmitModel.objects.create(parentForm=form, data=data)
        url = request.build_absolute_uri()
        print(request.META['HTTP_REFERER'], newSubmit)
        if (is_absolute(form.successRedirect)):
            url = form.successRedirect
        else:
            url = request.META['HTTP_REFERER'] + form.successRedirect
        return redirect(url)
    else:
        return JsonResponse({'status': 'error', 'code': 'method need to be POST'})
        
        
        
        
        
from urllib.parse import urlparse

def is_absolute(url):
    return bool(urlparse(url).netloc)