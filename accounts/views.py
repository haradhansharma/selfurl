from django.contrib import messages
from urllib.parse import urlparse
from django.http import Http404, HttpResponseRedirect
from .models import *
from .forms import UserCreationFormFront, PasswordChangeForm, UserForm, ProfileForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from doc.doc_processor import site_info
from django.contrib.auth import update_session_auth_hash


@login_required
def profile_setting(request, username): 
    
    
    title = username
    description = 'You can manage your personal information here.'
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('accounts:profile_setting', args=[str(username)])),
        'description': description,        
        'slogan': title, #it will work as a title as well.
             
    }    
    seo_info.update(modify)  
     
    if request.method == "POST":
        if 'user_form' in request.POST:
            user_form = UserForm(request.POST, instance=request.user)
                 
            if user_form.is_valid():                
                user_form.save()
                messages.success(request,('Your profile was successfully updated!'))                
            else:
                messages.error(request, 'Invalid form submission.')                
                messages.error(request, user_form.errors)    
                
        if 'profile_form' in request.POST:
            profile_form = ProfileForm(request.POST, instance=request.user.profile)   		    
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request,('Your profile data was successfully updated!'))
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, profile_form.errors)                 
                
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)     
    context = {
        "user":request.user,
        "user_form":user_form,
        "profile_form":profile_form,       
        'site' : seo_info ,
               
    }
    return render(request, 'registration/profile_settings.html', context = context)

@login_required
def password_change(request): 
    
    
    from doc.models import MetaText, Acordion
    
    meta_data = MetaText.objects.get(path='accounts:change_pass')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('accounts:change_pass')),
        'description': description,        
        'slogan': title,              
    }    
    seo_info.update(modify)   
    
    
    
    
    if request.method == "POST":        
        password_form = PasswordChangeForm(user=request.user, data=request.POST)        
        if password_form.is_valid():            
            password_form.save()            
            update_session_auth_hash(request, password_form.user)            
            messages.success(request,('Your password was successfully updated!')) 
        else:
            messages.error(request, 'Invalid form submission.')            
            messages.error(request, password_form.errors)         
        return HttpResponseRedirect(reverse('accounts:change_pass'))    
    password_form = PasswordChangeForm(request.user)  
    
    context = {
        "user":request.user,        
        "password_form":password_form,
        'meta_data' : meta_data ,
        'site' : seo_info ,
    }
    return render(request, 'registration/change_pass.html', context = context)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        from doc.models import MetaText, Acordion
    
        meta_data = MetaText.objects.get(path='accounts:password_reset_complete')   
        title = meta_data.title
        description = meta_data.description    
        
        seo_info = site_info() 
        modify = {
            'canonical' : self.request.build_absolute_uri(reverse('accounts:password_reset_complete')),
            'description': description,        
            'slogan': title + f" to {seo_info.get('domain')}"            
        }    
        seo_info.update(modify)   
        
        context['meta_data'] = meta_data
        context['site'] = seo_info
        
        return context

class CustomPasswordResetView(PasswordResetView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        from doc.models import MetaText, Acordion
    
        meta_data = MetaText.objects.get(path='accounts:password_reset')   
        title = meta_data.title
        description = meta_data.description    
        
        seo_info = site_info() 
        modify = {
            'canonical' : self.request.build_absolute_uri(reverse('accounts:password_reset')),
            'description': description,        
            'slogan': title + f" to {seo_info.get('domain')}"            
        }    
        seo_info.update(modify)   
        
        context['meta_data'] = meta_data
        context['site'] = seo_info
        
        return context
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        from doc.models import MetaText, Acordion
    
        meta_data = MetaText.objects.get(path='accounts:password_reset_done')   
        title = meta_data.title
        description = meta_data.description    
        
        seo_info = site_info() 
        modify = {
            'canonical' : self.request.build_absolute_uri(reverse('accounts:password_reset_done')),
            'description': description,        
            'slogan': title + f" to {seo_info.get('domain')}"            
        }    
        seo_info.update(modify)   
        
        context['meta_data'] = meta_data
        context['site'] = seo_info
        
        return context
    
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        
        from doc.models import MetaText, Acordion
    
        # meta_data = MetaText.objects.get(path='accounts:password_reset_confirm')   
        title = 'Confirm your new password'
        description = 'Please select a strong password and remember it for further use!  '
        
        seo_info = site_info() 
        modify = {
            'canonical' : self.request.build_absolute_uri(self.request.META['PATH_INFO']),
            'description': description,        
            'slogan': title + f" to {seo_info.get('domain')}"            
        }    
        seo_info.update(modify)   
        
        # context['meta_data'] = meta_data
        context['site'] = seo_info
        
        return context

    


class CustomLoginView(LoginView):
    #To avoid circular reference it is need to import here
    from .forms import LoginForm
    
    #overwriting form class to take control over default django
    form_class = LoginForm 
    
    #overwriting to set custom after login path
    next_page = ''
    
    #taking control over default of Django  
    def form_valid(self, form): 
        
        #set after login url 
        self.next_page = reverse_lazy('accounts:profile_setting', args=[str(form.get_user().username)])           
        
        #rememberme section        
        remember_me = form.cleaned_data.get('remember_me')     
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True  
        # self.request.session.set_test_cookie()
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        
        
        from doc.models import MetaText, Acordion
    
        meta_data = MetaText.objects.get(path='accounts:login')   
        title = meta_data.title
        description = meta_data.description    
        
        seo_info = site_info() 
        modify = {
            'canonical' : self.request.build_absolute_uri(reverse('accounts:login')),
            'description': description,        
            'slogan': title + f" to {seo_info.get('domain')}"            
        }    
        seo_info.update(modify)   
        
        context['meta_data'] = meta_data
        context['site'] = seo_info
        
        return context




def signup(request): 
    
    
    from doc.models import MetaText, Acordion
    
    meta_data = MetaText.objects.get(path='accounts:signup')   
    title = meta_data.title
    description = meta_data.description 
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('accounts:signup')),
        'description': description + f" at {seo_info.get('domain')}"  ,       
        'slogan': title + f" to {seo_info.get('domain')}"            
    }    
    seo_info.update(modify)  
    
    
           
    if request.method == 'POST':
        current_site = get_current_site(request)
        form = UserCreationFormFront(request.POST)
        if form.is_valid():     
            new_user = form.save(commit=False)    
            new_user.is_active = False       
            new_user.save()
            subject = 'Account activation required!' 
            message = render_to_string('emails/account_activation_email.html', {
                'user': new_user,                    
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),                
            })
            
            new_user.email_user(subject, message)            
            messages.success(request, 'Please Confirm your email to complete registration.') 
            return HttpResponseRedirect(reverse_lazy('login'))
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)
    else: 
        form = UserCreationFormFront()
    context = {
        'form': form,
        'meta_data' : meta_data ,
        'site' : seo_info ,      
        
    }
    return render(request, 'registration/register.html', context = context) 

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, ('Your account have been confirmed.'))
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        messages.warning(request, ('Activation link is invalid!'))
        return HttpResponseRedirect(reverse_lazy('home:home'))
        
    




    
    
    
    
    
    
    

