from django.shortcuts import render

def index(request):
	user = request.user
	logged_in = False
	if user.is_authenticated():
		logged_in = True
	context = { 'logged_in': logged_in }
	return render(request, 'info/index.html', context)
