from django.shortcuts import render

def test_view(request):
    return render(request, 'feed/index.html')

def feed_view(request):
	return render(request, 'feed/feed.html')