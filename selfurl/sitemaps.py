from django.contrib import sitemaps
from django.urls import reverse
from .models import *
from accounts.models import *
from contact.models import *
from doc.models import *
from selfurl.models import *

class SelfurlSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['accounts:signup', 'accounts:login', 'accounts:change_pass', 'accounts:password_reset_done','accounts:password_reset','accounts:password_reset_complete','contact:contact','doc:terms_and_conditions', 'doc:privacy_policy', 'selfurl:index','selfurl:report_malicious','selfurl:statistics', ] 

    def location(self, item):
        return reverse(item)      
    
class UserSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return User.objects.all() 
    
    def lastmod(self, obj):
        return obj.date_joined
        
    def location(self, obj):
        return "/accounts/%s"  % (obj.username)
    
class UrlLogsSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Shortener.objects.all() 
    
    def lastmod(self, obj):
        return obj.created
        
    def location(self, obj):
        return "/logs/%s"  % (obj.short_url)
    
class UrlSitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8    

    def items(self):
        return Shortener.objects.all() 
    
    def lastmod(self, obj):
        return obj.created
        
    def location(self, obj):
        return "/%s"  % (obj.short_url)
    
    

    
 
      
               
    