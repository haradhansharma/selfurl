from django.shortcuts import render
from . models import *
from django.http import JsonResponse
from django.utils import timezone

def lc(request):
    license = Licences.objects.all()
    
    context = dict()
    
    for l in license:
        if l.validaty < timezone.now():
            context.update({
                l.party_domain : False
            })
        else:
            context.update({
                l.party_domain : l.key
            })
    return JsonResponse(context)
            
            
            
    
