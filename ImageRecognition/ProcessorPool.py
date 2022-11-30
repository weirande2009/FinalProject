import ImageProcessor


class ProcessorPool:
    """
    An image processor pool
    """

    def __init__(self, worker_number: int):
        self.processors = []

    def recognize(self, image) -> str:
        pass

    def get_idle_worker(self) -> ImageProcessor:
        pass


