from django.shortcuts import render
from django.http import HttpResponse


def home(request):

    # return response_with_context(context)
    return HttpResponse("<h1>Yeah we know it works - home")


def events(request):

    return HttpResponse("<h1>Yeah we know it works - events")


def users(request):

    return HttpResponse("<h1>Yeah we know it works - users")

