from django.shortcuts import render

# Create your views here.
def index(request):
    title = "Broadcast"
    context = {'title': title, }
    return render(request, 'broadcast/index.html', context)
