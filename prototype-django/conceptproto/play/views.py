from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Video


def index(request):

    return render(request, 'play/index.html')

def video(request):

    if 'v' in request.GET:
        submitted_vid = request.GET['v']
        if  'v=' in submitted_vid:
            video_id_start = submitted_vid.find("v=") + 2
            video_id = submitted_vid[video_id_start:video_id_start+11]
            print(video_id)
            try:
                video = Video.objects.get(vid=video_id)
                print("#####", video)
            except:
                # 이 부분에서 새로 페이지 생성
                return HttpResponse('수정중')

        else:
            return HttpResponse('You submitted an wrong url.')
    else:
        return HttpResponse('You submitted an wrong url.')

    context = {'video':video}

    return render(request, 'play/video.html', context)
