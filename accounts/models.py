from django.forms import model_to_dict
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse




class User(AbstractUser):
    email = models.EmailField('E-Mail Address', unique=True)
    phone = models.CharField(max_length=252, null=True, blank=True)
    orgonization = models.CharField(max_length=252, null=True, blank=True)
     
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.email 
    
    def get_absolute_url(self):        
        return reverse('accounts:user_link', args=[str(self.username)])
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', verbose_name='user', on_delete=models.CASCADE)
    about = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    


