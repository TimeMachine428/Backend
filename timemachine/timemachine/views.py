#views cuz gotta view it lmao

from django.http import HttpResponse
import datetime

# This is our View function which receives info
# on the request
def hello_world(request):
 
    # Return a response object with the text Hello World
    return HttpResponse("Hello World")

def root_page(request):
 
    return HttpResponse("Root Home Page")

def html(request):
 
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)