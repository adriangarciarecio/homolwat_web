# IMPORTS
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader

##
# Handle 404 Errors
# @param request WSGIRequest list with all HTTP Request
def error404(request, *args, **kwargs):
    context = {}
    context["status"] = 404
    return render(request, 'home/error.html', context)

def error500(request):
    context = {}
    context["status"] = 500
    return render(request, 'home/error.html', context)

def error503(request):
    context = {}
    context["status"] = 503
    return render(request, 'home/error.html', context)

