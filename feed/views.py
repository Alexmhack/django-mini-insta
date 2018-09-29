import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from pusher import Pusher
from decouple import config

from .models import Feed
from .forms import DocumentForm

# instantiate pusher
pusher = Pusher(
	app_id=config("PUSHER_APP_ID"),
	key=config("PUSHER_APP_KEY"),
	secret=config("PUSHER_APP_SECRET"),
	cluster=config("PUSHER_APP_CLUSTER")
)

# Home page view with all feeds
def home_view(request):
	objects = Feed.objects.all().order_by('-id')
	context = {'objects': objects}
	return render(request, 'index.html', context)


# function to authenticate private channel
def pusher_authentication(request):
	channel = request.GET.get('channel_name', None)
	socket_id = request.GET.get('socket_id', None)
	auth = pusher.authenticate(
		channel=channel,
		socket_id=socket_id
	)

	return JsonResponse(json.dumps(auth), safe=False)


# function that triggers pusher request
def push_feed(request):
	# check if the method is post
	if request.method == "POST":
		form = DocumentForm(request.POST, request.FILES)
		if form.is_valid():
			description = form.cleaned_data.get("description")
			document = form.cleaned_data.get('document')
			try:
				pusher.trigger(
					'a_channel',
					'an_event',
					{'description': description, 'document': str(document)}
				)
			except Exception as e:
				print(e)
			form.save()
			return HttpResponse('ok')
		else:
			return form.ValidationError('form is not valid')

	else:
		return HttpResponse('error, please try again...')
