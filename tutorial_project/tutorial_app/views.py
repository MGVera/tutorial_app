from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	context_dict = {'boldmessage':'Tutorials here!'}

	return render(request, 'index.html', context_dict)

    
def about(request):
	return HttpResponse('About Us')