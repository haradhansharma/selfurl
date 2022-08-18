
from urllib.parse import urlparse, urlunparse
from django.conf import settings
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
from .models import Shortener, VisitorLog, ReportMalicious
import string
import random
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.safestring import mark_safe
import arrow


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
                user_agent = get_agent(request)       
                geodata = get_geodata(request)     
                if request.user.is_authenticated:
                    new_url = Shortener(long_url=long_url, short_url=check_exists(short_url), creator = request.user, ip = get_ip(request), user_agent = user_agent, country = geodata.get('country_code'),  lat = geodata.get('latitude'), long =  geodata.get('longitude'))
                else:
                    new_url = Shortener(long_url=long_url, short_url=check_exists(short_url), creator = None, ip = get_ip(request), user_agent = user_agent, country = geodata.get('country_code'),  lat = geodata.get('latitude'), long =  geodata.get('longitude'))                    
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
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)   
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
    
    
    results = {}
        
    if request.user_agent.is_mobile:
        user_usage = 'Mobile'        
    elif request.user_agent.is_tablet:
        user_usage = 'Tablet'    
    elif request.user_agent.is_touch_capable:
        user_usage = 'Touch Capable'
    elif request.user_agent.is_pc :
        user_usage = 'PC'
    elif request.user_agent.is_bot :
        user_usage = 'BOT'
    else:
        user_usage = 'Not able to figur out'        
    
    data = {
        'user_usage' : user_usage ,
        'user_browser' : request.user_agent.browser  ,
        'user_os' : request.user_agent.os ,
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
    from django_user_agents.utils import get_user_agent
    user_agent = get_user_agent(request)
    
    
    full_url = request.build_absolute_uri()
    parser_full = urlparse(full_url)    
    
    
    url = ''   
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
        
        #to accept api endpoint for registered users.
        if  parser_full.params or parser_full.query or parser_full.fragment:
            long_parse = urlparse(shortener.long_url)
            parts = (long_parse.scheme, long_parse.netloc, long_parse.path, parser_full.params, parser_full.query, parser_full.fragment, )
            redirect_to = urlunparse(parts)
        else:
            redirect_to = shortener.long_url 
         
        if creator:
            need_to_login = creator.last_login + timezone.timedelta(days=settings.LOGIN_REQUIRE_WITHIN_DAYS)
            if request.user_agent.is_bot:
                if  CURRENT_DATE_TIME <=  need_to_login: 
                    return HttpResponseRedirect(redirect_to) 
                else:
                    return HttpResponse({f'Your las login is {creator.last_login }, You supposed to login before {need_to_login} to get uninterepted service!'})
            else:
                return HttpResponseRedirect(redirect_to) 
            
            
                       
    except Exception as e:          
        raise Http404('Sorry this link is broken :(')
    
    title = f'{short_url}...........'
    description = 'Since destination was created by an unregistered user, so we are providing creator information that it is created from ip address: {}, country: {}, lat: {}, long: {} . You need to click on the button below to reach the destination. If you think it has been used for some malicious purpose, let us know by clicking the <a class="text-danger" target="_blank" href = "{}">Report Malicious</a>. We will take action!'.format(shortener.ip, shortener.country, shortener.lat, shortener.long, reverse('selfurl:report_malicious') ) 
    
    seo_info = site_info()  
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:redirect_url', args=[str(short_url)])),
        'description': description,        
        'slogan': title, #it will work as a title as well.             
    }    
    seo_info.update(modify) 
     
    
    context = {
        'redirecting' : f'Click To got to',
        'url' : url,        
        'site' : seo_info ,
        'visitor_log' : 'The url has been visited {} times from the various location of the internet world'.format(shortener.visitorlog_set.all().count()) 
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
                    url.save()
                    if not (ReportMalicious.objects.filter(url=url, user=request.user)).exists():
                        ReportMalicious.objects.create(url=url, user=request.user)
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
def allreport(request, short_url):
    reports = ReportMalicious.objects.filter(url = Shortener.objects.get(short_url = short_url)).order_by('created')
    created_since = arrow.get((reports.first()).created).humanize()
    page = request.GET.get('page', 1)
    paginator = Paginator(reports, 10)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    
    
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:allreport', args=[str(short_url)])),
        'description': "All reports submitted for this short URL as malicious are listed here.",  
        'slogan': f"All Reports of URL",   
                  
    }    
    seo_info.update(modify)  
    
    context = {
        'short_url': short_url,
        'site' : seo_info ,
        'reports' : reports,
        'created_since' : created_since
          
        
                
            }
    
    
    return render(request, 'selfurl/allreport.html', context=context)

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
    
    items = Shortener.objects.filter(creator = request.user).order_by('created')  
    # print((items.first()).created)
    
    created_since = arrow.get((items.first()).created).humanize()
    
    
    
    #Paginated response
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 10)
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
        'created_since' : created_since             
            }
    return render(request, 'selfurl/statistics.html', context = context)



@login_required
def log_details(request, short_url):
    seo_info = site_info() 
    modify = {
        'canonical' : request.build_absolute_uri(reverse('selfurl:log_details', args=[str(short_url)])),
        'description': "Every time someone clicks on your short URL, our technology will keep track. It doesn't matter if it came from the same device or from the same person.",  
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
        'reports':  ReportMalicious.objects.filter(url = shortener)[:10],
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
    