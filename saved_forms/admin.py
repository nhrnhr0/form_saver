from django.contrib import admin
from .models import FormModel, SubmitModel
# Register your models here.
class FormModelAdmin(admin.ModelAdmin):
    list_display= ('title', 'slug', 'notifyEmail', 'action_link')
    prepopulated_fields = {'slug': ('title',), }
admin.site.register(FormModel, FormModelAdmin)

class SubmitModelAdmin(admin.ModelAdmin):
    list_display= ('date', 'parentForm', 'data')
admin.site.register(SubmitModel, SubmitModelAdmin)