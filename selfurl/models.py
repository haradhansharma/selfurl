from pyexpat import model
from django.db import models
from accounts.models import User
from django.utils.text import slugify

class Shortener(models.Model):
    '''
    Creates a short url based on the long one    
    created -> Hour and date a shortener was created     
    times_followed -> Times the shortened link has been followed
    long_url -> The original link
    short_url ->  shortened link https://domain/(short_url)
    ''' 
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    times_followed = models.PositiveIntegerField(default=0)
    long_url = models.URLField(max_length=2000)
    short_url = models.SlugField(max_length=15, unique=True)
    active = models.BooleanField(default=True)
    remark = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    ip = models.CharField(max_length=152)
    user_agent = models.TextField()
    country = models.CharField(max_length=150)
    lat = models.CharField(max_length=150)
    long = models.CharField(max_length=150)

    class Meta:
        ordering = ["-created"]


    def __str__(self):
        return f'{self.long_url} to {self.short_url}'
    
    
    def save(self, *args, **kwargs):                           
        self.short_url = slugify(self.short_url)
        super().save(*args, **kwargs)
        
class VisitorLog(models.Model):
    shortener = models.ForeignKey(Shortener, on_delete=models.CASCADE)
    ip = models.CharField(max_length=152)
    user_agent = models.TextField()
    country = models.CharField(max_length=150)
    lat = models.CharField(max_length=150)
    long = models.CharField(max_length=150)
    visited = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ["-visited"]
        
        
    def __str__(self):
        return f'{self.shortener} from {self.ip}({self.country})'
    

        
    
