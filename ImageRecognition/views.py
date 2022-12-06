from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from ImageRecognition.ProcessorPool import ProcessorPool


def homepage(request):
    return render(request, "homepage.html")


def recognize(request):
    """
    Recognize an image
    :param request: http request
    :return: the image class name
    """
    image = request.FILES["image"]
    processor_pool = ProcessorPool()
    name = processor_pool.recognize(image)
    return JsonResponse({"name": name})
