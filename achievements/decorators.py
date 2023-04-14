from django.shortcuts import redirect
from django.http import HttpRequest
"""
Here we are creating a decorator to check whether the user is authenticated or not. 
We'll use this decorator where we believe logged-in users shouldn't be able to access it. 
As I mentioned, we create a function inside a function that we call a decorator, and to access a Django request, 
we again create another specific function that we call a "_wrapped_view". 
Here, we check if a user is authenticated; if it is, we return a redirect function. 
Otherwise, we redirect the original function the user is trying to access. 
"""

def user_not_authenticated(function=None, redirect_url='home'):
    def decorator(view_func):
        def _wrapped_view(request: HttpRequest, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    
    if function:
        return decorator(function)
    
    return decorator


def user_authenticated(function=None, redirect_url='signup_user'):
    def decorator(view_func):
        def _wrapper_function(requests: HttpRequest, *args, **kwargs):
            if not requests.user.is_authenticated:
                return redirect(redirect_url)
            return view_func(requests, *args, **kwargs)
        return _wrapper_function

    if function:
        return decorator(function)

    return decorator

    












