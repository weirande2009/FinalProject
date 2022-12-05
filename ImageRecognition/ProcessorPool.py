import ImageProcessor
import time


class ProcessorPool:
    """
    An image processor pool
    """

    def __init__(self, worker_number: int):
        self.processors = [ImageProcessor.ImageProcessor for i in range(worker_number)]
        self.imagePool = []
        self.visitedTimes = [0 for i in range(worker_number)]  # record how many times each worker is visited

    def recognize(self, image) -> str:

        self.imagePool.append(image)

        worker = self.get_idle_worker()
        if worker is None:
            return "504: timeout, can't find an idle worker"

        # update the visit times of current worker
        idx = self.processors.index(worker)
        self.visitedTimes[idx] += 1

        # delete this image, 'cause it has been processed
        self.imagePool.pop()

        res = worker.recognize(image)

        return res

    def get_idle_worker(self) -> ImageProcessor:

        for i in range(5):  # try at most 5 times
            for p in self.processors:
                if not p.busy:
                    return p

            # all processors are currently busy
            # wait 3 sec before finding a new idle processor/worker again
            print("all workers are currently occupied.\n")
            print("system will automatically find a new worker again in 3 sec...\n")
            time.sleep(3)

        # timeout
        return None

