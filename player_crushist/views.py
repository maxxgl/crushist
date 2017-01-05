from django.shortcuts import render
from django.http import HttpResponse


def index(request):

    # return response_with_context(context)
    return HttpResponse("<h1>Yeah we know it works")
