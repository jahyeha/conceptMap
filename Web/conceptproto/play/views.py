from django.shortcuts import render
import urllib
# Create your views here.

def index(request):
    return render(request, 'play/index.html')

def video(request):
    if 'v' in request.GET:
        submitted_vid = request.GET['v']
        print(submitted_vid)
        video_id = submitted_vid
    #title = urllib.urlopen("https://www.youtube.com/watch?v="+video_id)
    return render(request, 'play/video.html', {'video':video_id})
