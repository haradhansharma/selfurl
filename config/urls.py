from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = 'SELFURL admin'
admin.site.site_title = 'SELFURL admin'
# admin.site.site_url = ''
admin.site.index_title = 'SELFURL administration'
# admin.empty_value_display = '**Empty**'
'''
=====
DO NOT FORGET TO MAKE MIGRATION AFTER ADDING PATH! IT IS IMPORTNT!
=====
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('selfurl.urls')),
    path('', include('contact.urls')),
    path('', include('doc.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



