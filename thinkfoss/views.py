# Views.py
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from django.core.mail import send_mail
from django.core.mail.message import BadHeaderError
from django.http.response import HttpResponse

from thinkfoss import settings

def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view
