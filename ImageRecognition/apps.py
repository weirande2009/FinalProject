from django.apps import AppConfig


class ImagerecognitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ImageRecognition'

    # Before service starts
    def ready(self):
        pass



