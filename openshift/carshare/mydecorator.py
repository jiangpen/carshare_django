from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.sessions.backends.db import SessionStore
from django.template import loader, Context
from functools import wraps


def logged_already(extra_value="/admin"):
    def _my_decorator(view_func):
        def _decorator(request, *args, **kwargs):
            
			
						try:
							#import pdb; pdb.set_trace()
							#mm=s['member_id']
							mm=request.session.get('member_id', False)
							#print mm
							#import pdb; pdb.set_trace()
							if mm:
								response = view_func(request, *args, **kwargs)
								return response
							else:
								response = HttpResponseRedirect(extra_value)
								return response
						except KeyError:
							response = HttpResponseRedirect(extra_value)
							return response
            # maybe do something after the view_func call
            
						
        return wraps(view_func)(_decorator)
    return _my_decorator
    
"""
def logged_already(view_func):
    def _decorator(request, *args, **kwargs):
    	s = SessionStore()
			try:
				mm=s['member_id']
				response = view_func(request, *args, **kwargs)
        # maybe do something after the view_func call
        return response
				
			except KeyError:
				
				return False
        # maybe do something before the view_func call
       
    return wraps(view_func)(_decorator)
"""
   