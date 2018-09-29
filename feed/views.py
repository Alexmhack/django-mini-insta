from django.shortcuts import render

from .models import Feed

def home_view(request):
	objects = Feed.objects.all().order_by('-id')
	context = {'objects': objects}
	return render(request, 'home.html', context)
