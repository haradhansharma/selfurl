from django.shortcuts import render

from selfurl.decorators import coockie_required
from . forms import ContactForm
# from doc.models import ExSite
from django.core.mail import BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mass_mail
from doc.doc_processor import site_info
from django.urls import reverse

@coockie_required
def contact(request):    
    from doc.models import ExSite 
    
    
    from doc.models import MetaText, Acordion
    
    meta_data = MetaText.objects.get(path='contact:contact')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('contact:contact')),
        'description': description,        
        'slogan': title,              
    }    
    seo_info.update(modify)     
     
    if request.method == "POST":              
        form = ContactForm(request.POST)         
        if form.is_valid(): 
            # mail parameter   
            param =  ExSite.on_site.get()            
            
            # to user mail
            to_email = form.cleaned_data['email']
            to_name = form.cleaned_data['name']
            
            subject = 'We recived Your mail!'                
            message = 'Dear '+ to_name + '\n\n' + 'We have recived your message and will get back to you soon! \n\n' + 'Thank you for reachout.'   + '\n\n' + 'Best regards \n\n' + param.site.domain 
             
            # to admin mail           
            form_subject = f'{param.site.domain }-- Contact' + ' "' +  form.cleaned_data['subject'] +'"'                      
            form_message = form.cleaned_data['message'] 
            
            mail_list = [
                (subject, message, '', [to_email]) ,
                (form_subject, form_message, '', [param.email]) 
                ]
            
            send_mass_mail((mail_list), fail_silently=False) 
            form.save()
            messages.success(request, 'Contact request submitted successfully.')
            return redirect('contact:contact')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else:
        form = ContactForm()             
    context={
        'form':form,
        'meta_data' : meta_data ,
        'site' : seo_info ,
        
    }
    
    return render(request, 'contact/contact.html', context = context)