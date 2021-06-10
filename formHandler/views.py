from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FormModel, SubmitModel
from django.core.mail import EmailMessage
import json
# Create your views here.
@csrf_exempt
def handle_form_submition_view(request, uid):
    print('handle_form_submition_view: ', uid)
    if request.method=="POST":
        try:
            form = FormModel.objects.get(slug=uid)
        except:
            return JsonResponse({'status':'error', 'code': 'requested form not found'})
        data = {}
        messageBody = ''
        htmlMessage = '<table>'
        for key, value in request.POST.items():
            data[key]=value
            messageBody += key + ':\t' + value + '\n'
            htmlMessage += '<tr><td>' + key + '</td><td>' + value + '</td></tr>';
        
        newSubmit = SubmitModel.objects.create(parentForm=form, data=data)
        url = request.build_absolute_uri()
        print(request.META.get('HTTP_REFERER'), newSubmit)
        url = form.successRedirect
        
        dateStr = str(newSubmit.date.strftime("%Y-%m-%d %H:%M:%S"))
        messageBody += 'תאריך:\t' + dateStr;
        htmlMessage += '<tr><td> תאריך' + '</td><td>' + dateStr +  "</td></tr>";
        htmlMessage += '<tr><td colspan="2">' + 'ליד חדש נכנס לאתר, צורו קשר במהרה!' +  "</td></tr>";
        htmlMessage += '<tr><td colspan"2"> <a href="https://ms-global.co.il"><img src="https://lead.ms-global.co.il/logo_ms.png" style="height: 50px;" /> </a></td></tr>';
        
        n = SendEmailThread( title='הגשת טופס: ' + form.title + ' - ' + dateStr,
                             messageBody=messageBody,
                             htmlMessage=htmlMessage,
                             from_email='no-reply@ms-global.co.il',
                             to=[form.notifyEmail])
        n.start()
        #
        #email = EmailMessage(,messageBody,from_email='bot@ms-global.co.il', to=[form.notifyEmail])
        #print('email: ', email.send())
        return redirect(url)
    else:
        return JsonResponse({'status': 'error', 'code': 'method need to be POST'})
        
        
        
        
        
from urllib.parse import urlparse

def is_absolute(url):
    return bool(urlparse(url).netloc)


from threading import Thread
class SendEmailThread(Thread):

    def __init__ (self, title=None, messageBody=None, htmlMessage=None, from_email=None, to=None):
        Thread.__init__(self)
        self.title = title
        self.messageBody = messageBody
        self.html_message = htmlMessage,
        self.from_email = from_email
        self.to = to
    def run(self):        
        print('sending email to: ', self.to)
        email = EmailMessage(self.title,body=self.html_message[0],from_email=self.from_email, to=self.to)
        email.content_subtype = "html"
        print('email: ', email.send())