
from django.utils import timezone
from django.contrib import messages
import time
from django.shortcuts import redirect, render
from django.urls import reverse
from doc.doc_processor import site_info
import requests
import json
import selfurl
from .forms import ShortenerForm, CheckingForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Shortener, VisitorLog
import string
import random
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



CURRENT_DATE_TIME = timezone.now()

'''helper function'''
def random_digits():
    return "%0.3d" % random.randint(0, 999)
'''helper function'''
def check_exists(short_url):
    #make unique
    try:
        data = Shortener.objects.get(short_url = short_url)
        while data.short_url == short_url:
            return str(short_url) + str(random_digits())
    except:
        return short_url
    

def index(request):   
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='selfurl:index')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:index')),
        'description': description,        
        'slogan': title, #it will work as a title as well.
             
    }    
    seo_info.update(modify)  
    
    report_limit = seo_info.get('reported_url_limit')
   
    form = ShortenerForm()        
    if request.method == 'POST':
        form = ShortenerForm(request.POST)
        if form.is_valid():
            short_url = ''.join(random.choice(string.ascii_letters) for x in range(10))                    
            long_url = form.cleaned_data["long_url"]
            
            short_url = check_exists(short_url)
            
            '''
            if this url reported by anybody cannot be added further.            
            '''
            try:
                data = Shortener.objects.filter(long_url = long_url , active = False)
                if data.exists():
                    messages.error(request, f'The URL you are trying to shortened was reported as malicious! Request is rejected! Please be noted, if you have more than {int(report_limit)} reported url, your account can be banned!')
                    return HttpResponseRedirect(reverse('selfurl:index'))
            except:
                pass
            
            
            '''
            If this user shortend this url then will show that result
            Otherwise will save new and show new url
            '''
                
            try:                
                if request.user.is_authenticated:
                    data = Shortener.objects.get(long_url = long_url, creator = request.user)
                else:
                    data = Shortener.objects.get(long_url = long_url, creator = None)
                    
                     
                context = {            
                    'data': data,
                    'form': form,
                    'meta_data' : meta_data,
                    'site' : seo_info ,
                    'acordion':Acordion.objects.filter(path='selfurl:index')     
                    }
                return render(request, 'selfurl/index.html', context = context)
            except:
                if request.user.is_authenticated:
                    new_url = Shortener(long_url=long_url, short_url=check_exists(short_url), creator = request.user)
                else:
                    new_url = Shortener(long_url=long_url, short_url=check_exists(short_url), creator = None)                    
                new_url.save()   
                data = new_url  
                
                          
                context = {            
                    'data': data,
                    'form': form,
                    'meta_data': meta_data,
                    'site' : seo_info,
                    'acordion':Acordion.objects.filter(path='selfurl:index')           
                    }
                return render(request, 'selfurl/index.html', context = context)     
    context = {
        'form': form,
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='selfurl:index')           
    }
    return render(request, 'selfurl/index.html', context = context)

#helper functions
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:        
        ip = x_forwarded_for.split(',')[-1].strip()    
    elif request.META.get('HTTP_CLIENT_IP'):        
        ip = request.META.get('HTTP_CLIENT_IP')
    elif request.META.get('HTTP_X_REAL_IP'):        
        ip = request.META.get('HTTP_X_REAL_IP')
    elif request.META.get('HTTP_X_FORWARDED'):        
        ip = request.META.get('HTTP_X_FORWARDED')
    elif request.META.get('HTTP_X_CLUSTER_CLIENT_IP'):        
        ip = request.META.get('HTTP_X_CLUSTER_CLIENT_IP')
    elif request.META.get('HTTP_FORWARDED_FOR'):        
        ip = request.META.get('HTTP_FORWARDED_FOR')
    elif request.META.get('HTTP_FORWARDED'):        
        ip = request.META.get('HTTP_FORWARDED')
    elif request.META.get('HTTP_VIA'):        
        ip = request.META.get('HTTP_VIA')    
    else:        
        ip = request.META.get('REMOTE_ADDR')
        
    return ip
#helper function
def get_agent(request):
    from django_user_agents.utils import get_user_agent
    user_agent = get_user_agent(request)
    
    results = {}
        
    if user_agent.is_mobile:
        user_usage = 'Mobile'        
    elif user_agent.is_tablet:
        user_usage = 'Tablet'    
    elif user_agent.is_touch_capable:
        user_usage = 'Touch Capable'
    elif user_agent.is_pc :
        user_usage = 'PC'
    elif user_agent.is_bot :
        user_usage = 'BOT'
    else:
        user_usage = 'Not able to figur out'        
    
    data = {
        'user_usage' : user_usage        
    }    
    results.update(data)
    
    data = {
        'user_browser' : request.user_agent.browser        
    }    
    results.update(data)
    
    data = {
        'user_os' : request.user_agent.os       
    }    
    results.update(data)
    
    data = {
        'user_device' : request.user_agent.device      
    }    
    results.update(data)
    
    return results
    
    
    
    
    
    
#helper function
def get_geodata(request): 
    ip_address = get_ip(request)
    # URL to send the request to
    request_url = 'https://geolocation-db.com/jsonp/' + ip_address
    # Send request and decode the result
    response = requests.get(request_url)
    result = response.content.decode()
    # Clean the returned string so it just contains the dictionary data for the IP address
    result = result.split("(")[1].strip(")")
    # Convert this data into a dictionary
    result  = json.loads(result)
    return result
    


def redirect_url(request, short_url):
    url = ''
    
    
    title = 'Redirecting...........'
    description = 'If the Url was made anonymously, it will take 5 seconds to load; else, it will load immediately!'  
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:redirect_url', args=[str(short_url)])),
        'description': description,        
        'slogan': title, #it will work as a title as well.             
    }    
    seo_info.update(modify) 
    
    try:        
        shortener = Shortener.objects.get(short_url=short_url, active = True)
        creator = shortener.creator        
        url += shortener.long_url
        shortener.times_followed += 1
        shortener.save()
        
        user_agent = get_agent(request)       
        geodata = get_geodata(request)        
        VisitorLog.objects.create(
            shortener=shortener, 
            ip = get_ip(request), 
            user_agent = user_agent, 
            country = geodata.get('country_code'), 
            lat = geodata.get('latitude'), 
            long =  geodata.get('longitude')
            
            )
        
                
        if creator:        
            return HttpResponseRedirect(shortener.long_url)
                       
    except Exception as e:        
        raise Http404('Sorry this link is broken :(')
     
    
    context = {
        'redirecting' : 'Redirecting...........',
        'url' : url,        
        'site' : seo_info ,
            }
    return render(request, 'selfurl/redirecting.html', context = context)

   
@login_required
def report_malicious(request):   
    
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='selfurl:report_malicious')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:report_malicious')),
        'description': description,        
        'slogan': title, #it will work as a title as well.             
    }    
    seo_info.update(modify)  
    
    
    form = CheckingForm()        
    if request.method == 'POST':        
        form = CheckingForm(request.POST)
        if form.is_valid():           
            '''               
            we will find all orginal url based on the supplied short url and all url will be deactivated               
            '''                 
            short_url = form.cleaned_data["short_url"]
            url = Shortener.objects.filter(short_url = short_url)            
            if url.exists():   
                all_long_url =  Shortener.objects.filter(long_url = url.first().long_url)            
                for url in all_long_url:
                    url.active = False
                    if not url.remark:
                        url.remark = f'{request.user.username} Reported on {CURRENT_DATE_TIME} <br>'                        
                    else:
                        url.remark += f'{request.user.username} Reported on {CURRENT_DATE_TIME} <br>' 
                    url.save()
                messages.warning(request, f'We have blocked this url and it is not aviable now! Stay Safe! ')
            else:
                messages.warning(request, f'This url not found in our record!')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)    
                
    
    context = {
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='selfurl:report_malicious') ,  
        'form' : form
                
            }
    return render(request, 'selfurl/report_melicious.html', context = context)

@login_required
def statistics(request):
    
    from doc.models import MetaText, Acordion
    meta_data = MetaText.objects.get(path='selfurl:statistics')   
    title = meta_data.title
    description = meta_data.description    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:statistics')),
        'description': description,        
        'slogan': title, #it will work as a title as well.             
    }    
    seo_info.update(modify)  
    
    items = Shortener.objects.filter(creator = request.user)  
    
    #Paginated response
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 6)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    
    
    context = {                
        'items' : items ,
        'meta_data' : meta_data ,
        'site' : seo_info ,
        'acordion':Acordion.objects.filter(path='selfurl:statistics') ,                 
            }
    return render(request, 'selfurl/statistics.html', context = context)




def log_details(request, short_url):
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:log_details', args=[str(short_url)])),
        'description': "Every time someone clicks on your short URL, our technology will keep track. It doesn't matter if it came from the same device or from the same person.",        
        'slogan2': f"Visitor Logs of shorten URL-{short_url}", #it will work as a title as well.    
        'slogan': f"Visitor Logs of shorten URL",         
    }    
    seo_info.update(modify)  
    
    shortener = Shortener.objects.get(short_url = short_url)
    visit_logs = VisitorLog.objects.filter(shortener = shortener)  
    #Paginated response
    page = request.GET.get('page', 1)
    paginator = Paginator(visit_logs, 3)
    try:
        visit_logs = paginator.page(page)
    except PageNotAnInteger:
        visit_logs = paginator.page(1)
    except EmptyPage:
        visit_logs = paginator.page(paginator.num_pages)
        
        # Every time someone clicks on your short URL, our technology will keep track. It doesn't matter if it came from the same device or from the same person.
        # Visitor Logs of shorten URL-
    
    context = {     
        
        'site' : seo_info ,                  
        'visit_logs' : visit_logs ,
        'short_url' : short_url,
        'remark':  shortener.remark,
        'clicked':  shortener.times_followed          
            }
    return render(request, 'selfurl/log_details.html', context = context)
    

def dispute_report(request):
    '''
    we will take dispute against reported url.
    dispute will be save in separate database in admin.
    will check manually dispute.
    if dispute agreed then all url will be activated from admin
    '''
    pass
    