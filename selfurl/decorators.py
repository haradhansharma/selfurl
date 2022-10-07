def coockie_exempts(function):
    def wrap(request, *args, **kwargs): 
        if 'term_accepted' in request.session:   
            del request.session['term_accepted']       
        return function(request, *args, **kwargs)         
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap


def coockie_required(function):
    def wrap(request, *args, **kwargs):  
        if 'term_accepted' not in request.session:   
            request.session['term_accepted'] = False             
        if request.GET.get('term_accepted'):
            request.session['term_accepted'] = True 
        return function(request, *args, **kwargs)         
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap