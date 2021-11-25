from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EmailNotify, FormModel, SubmitModel, TelegramNotify

class EmailNotifyAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')
    search_fields = ('email','name')
admin.site.register(EmailNotify, EmailNotifyAdmin)



class TelegramNotifyAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'name')
    search_fields = ('chat_id','name')
admin.site.register(TelegramNotify, TelegramNotifyAdmin)


    # Register your models here.
class FormModelAdmin(admin.ModelAdmin):
    list_display= ('title','action_link_tag', 'action_link','slug','get_absolute_url')
    prepopulated_fields = {'slug': ('title',), }
    filter_horizontal = ('notifyEmails','notifyTelegram',)
admin.site.register(FormModel, FormModelAdmin)

class SubmitModelAdmin(admin.ModelAdmin):
    list_display= ('date', 'parentForm', 'data')
admin.site.register(SubmitModel, SubmitModelAdmin)