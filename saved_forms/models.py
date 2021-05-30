from django.db import models
from django.db.models.base import ModelBase
from django.contrib.sites.models import Site
# Create your models here.
class FormModel(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=False, null=False)
    notifyEmail = models.EmailField()
    def __str__(self):
        return self.title
        
    @property
    def action_link(self):
        domain = Site.objects.get_current().domain
        return domain + '/submit/' + self.slug

class SubmitModel(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    parentForm = models.ForeignKey(to=FormModel, on_delete=models.CASCADE)
    data = models.JSONField()
    
    def __str__(self):
        return str(self.parentForm) + ' (' + str(self.id) + ')'