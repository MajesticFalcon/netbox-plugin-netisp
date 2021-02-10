from django.urls import path
from django.http import HttpResponse



def dummy_view(request):
    htm1l = "<html><body>Net ISP Home.</body></html>"
    return HttpResponse(htm1l)


urlpatterns = [
    path("", dummy_view, name="home"),
]