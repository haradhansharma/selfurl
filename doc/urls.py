from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

'''
=====
DO NOT FORGET TO MAKE MIGRATION AFTER ADDING PATH! IT IS IMPORTNT!
=====
'''

app_name = 'doc'

urlpatterns = [
    path('su/webmanifest/', views.webmanifest, name='webmanifest'),
    path('su/terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('su/privacy-policy/', views.privacy_policy, name='privacy_policy'),  
    
] 


# def get_doc_urls():        
#         url_list = []
#         for url in urlpatterns:        
#             path_name = (
#                 str(app_name + ':' + url.name) , str(url.name.capitalize())  ,          
#             )
#             url_list.append(path_name)
#             # url_list.append(url.pattern._regex) if isinstance(url.pattern, RegexPattern) else url_list.append(url.pattern._route)        
#         return url_list   
    
def get_doc_urls():        
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
