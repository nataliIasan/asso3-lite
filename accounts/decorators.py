from django.contrib.auth.decorators import login_required as _login_required
from django.shortcuts import redirect
from functools import wraps

login_required = _login_required

def role_required(expected):
    def deco(view):
        @wraps(view)
        def _wrapped(request,*a,**k):
            if not request.user.is_authenticated:
                return redirect('login')
            if getattr(request.user,'role',None) != expected:
                return redirect('landing')
            return view(request,*a,**k)
        return _wrapped
    return deco
