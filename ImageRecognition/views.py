from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ImageRecognition.ProcessorPool import ProcessorPool
import os


def homepage(request):
    return render(request, "homepage.html")


@csrf_exempt
def recognize(request):
    """
    Recognize an image
    :param request: http request
    :return: the image class name
    """
    image = request.FILES.get("file")
    img_name = image.name
    with open(img_name, "wb") as f:
        for chunk in image.chunks():
            f.write(chunk)

    processor_pool = ProcessorPool()
    name = processor_pool.recognize(img_name)
    os.remove(img_name)
    return JsonResponse({"name": name})
