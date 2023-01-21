
from django.urls import path
from . import views


'''
=====
DO NOT FORGET TO MAKE MIGRATION AFTER ADDING PATH! IT IS IMPORTNT!
=====
'''

app_name = 'contact'


urlpatterns = [
    path('contact/', views.contact, name='contact'),  
    
]


    
def get_contact_urls():        
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

