from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from doc.models import ExSite
from doc.doc_processor import site_info



def webmanifest(request):
    site = ExSite.on_site.get()    
    icons = []    
    ic192 = {
        "src": site.og_image.url,
        "sizes": "192x192",
        "type": "image/png"        
    }
    
    icons.append(ic192)   
    ic512 = {
        "src": site.og_image.url,
        "sizes": "512x512",
        "type": "image/png"        
    }
    icons.append(ic512)    
    site_info = {
        'name' : site.site.name,
        'short_name' : site.site.name,
        'icons' : icons,
        # 'meta_name': site.site_meta,
        # 'description': site.site_description,
        # 'tag': site.site_meta_tag,
        # 'favicon': site.site_favicon.url,
        # 'logo': site.site_logo.url,
        # 'slogan': site.slogan,
        # 'og_image': site.og_image.url,
        # 'phone': site.phone,
        # 'email': site.email,
        # 'location': site.location,
        # 'facebook_link': site.facebook_link,
        # 'twitter_link': site.twitter_link,
        # 'linkedin_link': site.linkedin_link,
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "display": "standalone"        
    }
    
    return JsonResponse(site_info, safe=False)

def terms_and_conditions(request):
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='doc:terms_and_conditions')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('doc:terms_and_conditions')),
        'description': description,        
        'slogan': title, #it will work as a title as well.
             
    }    
    seo_info.update(modify)  
    context = {
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='doc:terms_and_conditions') 
    }
    return render(request, 'doc/terms.html', context = context)

def privacy_policy(request):
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='doc:privacy_policy')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('doc:privacy_policy')),
        'description': description,        
        'slogan': title, #it will work as a title as well.
             
    }    
    seo_info.update(modify)  
    context = {
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='doc:privacy_policy') 
    }
    return render(request, 'doc/privacy.html', context = context)


    
