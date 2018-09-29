# django-mini-insta
We will make a photo feed using Django and Pusher. This is like a mini Instagram, but 
without the comments and filter functionality.

In this tutorial we will go through **django** and [pusher](https://pusher.com)
At the end of this project we will have a photo feed project just like mini intagram
but with fewer functionality excluding comments and filters.

# Django Setup
I hope you have some understanding of [django](https://www.djangoproject.com/). And for pusher refer to its [documentation](https://pusher.com/docs)

```
django-admin startproject photofeed .
```

```
python manage.py startapp feed
```

Add app in project settings.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'feed',
]
```

Now run the server

```
python manage.py runserver
```

# Create App On Pusher
Go to [Pusher](https://puhser.com) and login or signup. The create new app with name
```django-photo-feed``` with ```Jquery``` as **frontend** and ```Django``` as 
**backend** and add any description that you like in the bottom.

Pusher has its own python sdk, install it using

```
pip install pusher
```

Pusher: This is the official Pusher library for Python. We will be using this library 
to trigger and send our messages to the Pusher HTTP API

# Feed Model
In ```models.py``` file inside **feed** app create model for our mini-instagram project

```
from django.db import models

class Feed(models.Model):
	description = models.CharField(max_length=255, blank=True)
	document = models.ImageField(upload_to='static/documents')
```

In the above block of code, we defined a model called Feed. The Feed table will consist of the following fields:

1. A field to store the description of the photo
2. A field to store the photo

**Notice** we can alos use ```FileField``` but we ```ImageField``` is recommended 
since we will need only images to be uploaded by users.```upload_to``` argument takes 
the path to which the file will be uploaded. Please note that this path is relative 
to the path of the ```DJANGO MEDIA ROOT```, which we will set now.

Now we will be setting the ```MEDIA_ROOT``` variable in ```photofeed/settings.py``` file 

```
...
MEDIA_ROOT = os.path.join(BASE_DIR, 'feed/')
```

Add this piece of code to the bottom of file. We are setting the path to ```feed``` 
app folder and the ```upload_to``` argument uploads to ```static/documents``` which 
will be inside the **feed** folder.

# Feed View
Open **feed/views.py** file add

```
import json

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from pusher import Pusher

from .forms import *

#instantiate pusher
pusher = Pusher(app_id='XXX_APP_ID', key='XXX_APP_KEY', secret='XXX_APP_SECRET', cluster='XXX_APP_CLUSTER')

# Create your views here.

# function that serves the welcome page
def index(request):
    # get all current photos ordered by the latest
    all_documents = Feed.objects.all().order_by('-id')
    # return the index.html template, passing in all the feeds
    return render(request, 'index.html', {'all_documents': all_documents})


#function that authenticates the private channel 
def pusher_authentication(request):
    channel = request.GET.get('channel_name', None)
    socket_id = request.GET.get('socket_id', None)
    auth = pusher.authenticate(
      channel = channel,
      socket_id = socket_id
    )

    return JsonResponse(json.dumps(auth), safe=False)


#function that triggers the pusher request
def push_feed(request):
    # check if the method is post
    if request.method == 'POST':
        # try form validation
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            # trigger a pusher request after saving the new feed element 
            pusher.trigger('a_channel', 'an_event', {'description': f.description, 'document': f.document.url})
            return HttpResponse('ok')
        else:
            # return a form not valid error
            return HttpResponse('form not valid')
    else:
       # return error, type isnt post
       return HttpResponse('error, please try again')
```

The above code is self explanatory.

In the index function, we fetch all the available photos in the database. The photos 
are then rendered in the view. This enables a new user to see all previous feeds 
that are available. In the pusher_authentication function, we verify that the 
current user can access our private channel. In the push_feed function, we check if 
it is a POST request, then we try validating our form before saving it into the 
database. (The form used in this method named DocumentForm is not available yet. We 
will be creating it soon.) After the form validation, we then place our call to the 
Pusher library for realtime interaction.

# Create Form 
Create a new file inside **feed** app named ```forms.py``` and inside it 

```
from django import forms

from .models import Feed

class DocumentForm(forms.ModelForm):
	class Meta:
		model = Feed
		fields = "__all__"
```

In the above code block, we have imported our Feed model and used it to create a 
form. This form will now handle the validation and upload of images to the right 
folder.
