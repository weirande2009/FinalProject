from django.apps import AppConfig
from ProcessorPool import ProcessorPool


class ImagerecognitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ImageRecognition'
    WORKER_NUMBER = 4

    # Before service starts
    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        self.processor_pool = ProcessorPool(self.WORKER_NUMBER)

    # Before service starts
    def ready(self):
        pass



