from django.contrib import admin
from django.urls import path

from feed.views import home_view, pusher_authentication, push_feed

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', home_view, name='home'),
    path('push-feed/', push_feed, name='push-feed'),
    path('push-authentication/', pusher_authentication, name='push-authentication'),
]
