from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.apps import apps


def homepage(request):
    return render(request, "homepage.html")


def recognize(request):
    """
    Recognize an image
    :param request: http request
    :return: the image class name
    """
    image = request.FILES["image"]
    name = apps.get_app_config('ImageRecognition').processor_pool.recognize(image)
    return JsonResponse({"name": name})
