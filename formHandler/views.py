from threading import Thread
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from server.secrects import TELEGRAM_BOT_TOKEN
from .models import FormModel, SubmitModel
from django.core.mail import EmailMessage
import json
# Create your views here.

def generate_email_body(data, dateStr):
    messageBody = ''
    htmlMessage = '<table>'
    for d in data:
        key = d
        value = data[key]
        
        messageBody += key + ':\t' + value + '\n'
        htmlMessage += '<tr><td>' + key + '</td><td>' + value + '</td></tr>';
    
    messageBody += 'תאריך:\t' + dateStr;
    htmlMessage += '<tr><td> תאריך' + '</td><td>' + dateStr +  "</td></tr>";
    htmlMessage += '<tr><td colspan="2">' + 'ליד חדש נכנס לאתר, צרו קשר במהרה!' +  "</td></tr>";
    htmlMessage += '<tr><td colspan"2"> <a href="https://ms-global.co.il"><img src="https://lead.ms-global.co.il/logo_ms.png" style="height: 50px;" /> </a></td></tr>';
    return [
            messageBody,
            htmlMessage,
    ]


def generate_telegram_message(title, data, dateStr):
    message = '\n'
    message += 'טופס חדש הוגש ב ' + title + ' \n'
    for d in data:
        key = d
        value = data[key]
        
        message += key + ':\t ' + value + ' \n'
    message += dateStr + '\n';
    return message

@csrf_exempt
def handle_form_submition_view(request, uid):
    print('handle_form_submition_view: ', uid)
    if request.method=="POST":
        try:
            form = FormModel.objects.get(slug=uid)
        except:
            return JsonResponse({'status':'error', 'code': 'requested form not found'})
        '''
        data = {}
        messageBody = ''
        htmlMessage = '<table>'
        for key, value in request.POST.items():
            data[key]=value
            messageBody += key + ':\t' + value + '\n'
            htmlMessage += '<tr><td>' + key + '</td><td>' + value + '</td></tr>';
        '''
        #data = request.POST.items()
        data={}
        for key, value in request.POST.items():
            data[key]=value
        newSubmit = SubmitModel.objects.create(parentForm=form, data=data)
        url = request.build_absolute_uri()
        print(request.META.get('HTTP_REFERER'), newSubmit)
        url = form.successRedirect
        
        
        
        # get all the emails from the form
        emails = list(form.notifyEmails.all().values_list('email', flat=True))
        
        dateStr = str(newSubmit.date.strftime("%Y-%m-%d %H:%M:%S"))
        
        [messageBody,htmlMessage]  = generate_email_body(data, dateStr)
        
        # send the email to all the list in a new thread
        
        n = SendEmailThread( title='הגשת טופס: ' + form.title + ' - ' + dateStr,
                             messageBody=messageBody,
                             htmlMessage=htmlMessage,
                             from_email='Main@ms-global.co.il',
                             to=emails)
        n.start()
        
        
        
        # get all the chat ids from the form
        chat_ids = list(form.notifyTelegram.all().values_list('chat_id', flat=True))
        message = generate_telegram_message(form.title, data, dateStr)
        n2 = SendTelegramThread(chat_ids=chat_ids, message=message)
        n2.start()
        
        return redirect(url)
    else:
        return JsonResponse({'status': 'error', 'code': 'method need to be POST'})
        
        
        
        
        
from urllib.parse import urlparse

def is_absolute(url):
    return bool(urlparse(url).netloc)

class SendTelegramThread(Thread):
    def __init__(self, chat_ids, message):
        Thread.__init__(self)
        self.chat_ids = chat_ids
        self.message = message
        
    def run(self):
        import telegram
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        for chat_id in self.chat_ids:
            print(bot.send_message(chat_id=chat_id, text=self.message, parse_mode='HTML'))
    
from threading import Thread
class SendEmailThread(Thread):

    def __init__ (self, title, messageBody, htmlMessage, from_email, to):
        
        Thread.__init__(self)
        self.title = title
        self.messageBody = messageBody
        self.html_message = htmlMessage
        self.from_email = from_email
        self.to = to
    def run(self):        
        print('sending email to: ', self.to)
        email = EmailMessage(self.title,body=self.html_message,from_email=self.from_email, to=self.to)
        email.content_subtype = "html"
        print('email: ', email.send())