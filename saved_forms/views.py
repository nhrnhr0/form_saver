from django.shortcuts import render
from .models import FormModel, SubmitModel
# Create your views here.
def handle_form_submition_view(request, uid):
    
    form = FormModel.objects.get(slug=uid)
    if request.method=="POST":
        for key, value in request.POST.items():
            print(f'Key: {key}') 
            print(f'Value: {value}') 