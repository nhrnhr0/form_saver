from typing import get_args
from django.db import models
from django.utils.html import mark_safe

# Create your models here.
from django.db import models
from django.db.models.base import ModelBase
from django.contrib.sites.models import Site
from django.urls import reverse

class EmailNotify(models.Model):
    email = models.EmailField(max_length=254)
    name = models.CharField(max_length=100, blank=True, null=True)
    class Meta():
        unique_together = ('email','name',)
    def __str__(self):
        return self.name + " - " + self.email

class TelegramNotify(models.Model):
    chat_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    class Meta():
        unique_together = ('chat_id','name',)
    def __str__(self):
        return self.name + " - " + self.chat_id
    
# Create your models here.
class FormModel(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=False, null=False)
    #notifyEmail = models.EmailField()
    notifyEmails = models.ManyToManyField(EmailNotify, blank=True)
    notifyTelegram = models.ManyToManyField(TelegramNotify, blank=True)
    successRedirect = models.URLField(default='/success')
    def __str__(self):
        return self.title
    
    @property
    def action_link(self):
        domain = Site.objects.get_current().domain
        return domain + self.get_absolute_url();
    @property
    def action_link_tag(self):
        return mark_safe(f'<a href="{self.action_link}"> {self.action_link}</a>')
    def get_absolute_url(self):
        return reverse("form-submition", kwargs={"uid": self.slug})
    

class SubmitModel(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    parentForm = models.ForeignKey(to=FormModel, on_delete=models.CASCADE)
    data = models.JSONField()
    
    def __str__(self):
        return str(self.parentForm) + ' (' + str(self.id) + ')'