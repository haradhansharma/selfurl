from . models import *
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox

class ContactForm(forms.ModelForm):    
    class Meta:
        model = Contacts
        fields = ['name', 'email', 'subject', 'message'] 
        widgets = {
        'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class':'form-control'}),
        'email': forms.TextInput(attrs={'placeholder': 'Your Email', 'class':'form-control'}),
        'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class':'form-control'}),
        'message': forms.Textarea(attrs={'placeholder': 'Message', 'class':'form-control', 'style':"height: 150px;"}),
    }
        
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)  
    