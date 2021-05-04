from django.shortcuts import render, HttpResponse
from django.utils.translation import gettext as _


# Create your views here.

def index(request):
    o = _("Hello")
    return HttpResponse(o)
