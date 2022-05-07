from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings


class Contacts(models.Model):
    site = models.ForeignKey(Site, related_name='contacts', verbose_name='ContactsTo', on_delete=models.CASCADE, default=settings.SITE_ID)
    name = models.CharField(max_length=100, verbose_name='Enter Name' ) 
    email = models.EmailField(unique=False, verbose_name='Enter Email')
    subject = models.CharField(max_length=256, verbose_name='Subject')
    message = models.TextField(max_length=1000, verbose_name='Messages')
    
    
    
    def __str__(self):
        return self.message