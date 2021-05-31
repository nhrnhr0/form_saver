from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FormModel, SubmitModel
# Register your models here.
class FormModelAdmin(admin.ModelAdmin):
    list_display= ('title','action_link_tag', 'action_link','slug', 'notifyEmail','get_absolute_url')
    prepopulated_fields = {'slug': ('title',), }
admin.site.register(FormModel, FormModelAdmin)

class SubmitModelAdmin(admin.ModelAdmin):
    list_display= ('date', 'parentForm', 'data')
admin.site.register(SubmitModel, SubmitModelAdmin)