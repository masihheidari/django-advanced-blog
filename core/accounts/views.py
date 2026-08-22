from django.shortcuts import render
from django.http import HttpResponse
import time
from .tasks import sendmail

def send_email(request):
    sendmail.delay()
    return HttpResponse('<h1> done sending </h1>')