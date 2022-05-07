from django import forms
from .models import Shortener
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError


class ShortenerForm(forms.ModelForm):    
    long_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "form-control border-0 rounded-pill w-100 ps-4 pe-5", "placeholder": "Your URL to shorten", 'style':"height: 48px;"}))
    
    
    class Meta:
        model = Shortener
        fields = ('long_url',)
        

class CheckingForm(forms.Form):   
    from django.contrib.sites.models import Site
    
    short_url = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(
        attrs={"class": "form-control border-0 w-100 ps-4 pe-5", 'placeholder': "Enter last part of url" , 'style':"height: 48px; border-radius: 0px;"}),
        label=Site.objects.get_current().domain + '/'
        )
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)  
    
     