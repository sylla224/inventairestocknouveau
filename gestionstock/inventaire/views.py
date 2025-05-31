from django.shortcuts import render

# Create your views here.
def index(request):
    """
    Render the index page of the inventory application.
    """
    return render(request, 'inventaire/index.html')
