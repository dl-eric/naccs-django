from django.http import HttpResponseRedirect
from django.conf import settings

def logout_required(view):
    def f(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return view(request, *args, **kwargs)
    return f