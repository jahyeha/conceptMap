from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):

    # context = {}
    return render(request, 'play/index.html')
    # return HttpResponse("hello")

def videos(request, video_id):
    # print("#####", video_id)
    # return HttpResponse("hello")
    return render(request, 'play/video.html')
