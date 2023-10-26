from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_view, name='test_view'),
	path('feed/', views.feed_view, name='feed_view'),
]
