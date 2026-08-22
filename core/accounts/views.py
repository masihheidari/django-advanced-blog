from django.http import HttpResponse
from .tasks import sendmail


def send_email(request):
    sendmail.delay()
    return HttpResponse("<h1> done sending </h1>")
