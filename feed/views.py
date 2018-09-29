from django.shortcuts import render
from django.http import JsonResponse
from pusher import Pusher

from .models import Feed

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
	return render(request, 'home.html', context)


# function to authenticate private channel
def pusher_authentication(request):
	channel = request.GET.get('channel_name', None)
	socket_id = request.GET.get('socket_id', None)
	auth = pusher.authenticate(
		channnel=channel,
		socket_id=socket_id
	)

	return JsonResponse(json.dumps(auth), safe=False)
