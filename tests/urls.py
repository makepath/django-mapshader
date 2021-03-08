from django.urls import path, include


urlpatterns = [
    path('', include('django_mapshader.urls', namespace='django_mapshader')),
]
