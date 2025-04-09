from django.shortcuts import render

# Create your views here.
def index(request):
    """ Shows the index/home/dashboard page """
    return render(request, "app/index.html", {"idk": "yeah"})
