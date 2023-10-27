from django.urls import path
from . import views

urlpatterns = [
    path('', views.core_render, name="Index Page"),
	path('feed/', views.feed_render, name="Feed Page"),
]
