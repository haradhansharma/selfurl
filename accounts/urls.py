
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, PasswordChangeView 
from .forms import LoginForm


app_name = 'accounts'
'''
=====
DO NOT FORGET TO MAKE MIGRATION AFTER ADDING PATH! IT IS IMPORTNT!
=====
'''

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html',  authentication_form=LoginForm), name='login'), 
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),   
    path('<str:username>', views.profile_setting, name='profile_setting'), 
    path('change_pass/', views.password_change, name='change_pass'),   
    
]

def get_accounts_urls():        
        url_list = []        
        for url in urlpatterns:  
            #skipping url with arguments            
            c = [url for i in str(url.pattern ).split('/')  if i.startswith('<')  ]             
            if url not in c :         
                path_name = (
                str(app_name + ':' + url.name) , str(url.name.capitalize())  ,          
                )
                url_list.append(path_name)        
                 
        return url_list 











