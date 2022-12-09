import threading

from ImageRecognition import ImageProcessor
import time
from .models import Status


class Singleton(object):
    WORKER_NUMBER = 4

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(self.WORKER_NUMBER)
        return self._instance[self._cls]


@Singleton
class ProcessorPool:
    """
    An image processor pool
    """
    CONFIG_FILE_NAME = "worker_config"

    def __init__(self, worker_number: int):
        worker_address = self.read_config()
        self.processors = [ImageProcessor.ImageProcessor(worker_address[i][0], worker_address[i][1]) for i in range(
            worker_number)]
        self.imagePool = []
        self.visitedTimes = [0 for i in range(worker_number)]  # record how many times each worker is visited
        self.lock = threading.Lock()
        all_status = Status.objects.all()
        if len(all_status) == 0:
            for i in range(worker_number):
                Status.objects.create(id=str(i), status=True)
        else:
            for status in all_status:
                status.status = True
                status.save()

    def recognize(self, image) -> str:

        self.imagePool.append(image)

        worker, status = self.get_idle_worker()
        if worker is None:
            return "504: timeout, can't find an idle worker"

        # update the visit times of current worker
        idx = self.processors.index(worker)
        self.visitedTimes[idx] += 1

        # delete this image, 'cause it has been processed
        self.imagePool.pop()

        res = worker.recognize(image)

        self.lock.acquire()
        status.status = True
        status.save()
        self.lock.release()

        return res

    def get_idle_worker(self) -> (ImageProcessor, Status):
        for i in range(5):  # try at most 5 times
            self.lock.acquire()
            print("Processors' state: ", end="")
            all_status = Status.objects.all()

            for status in all_status:
                print(str(status.status) + " ", end="")
            for index, status in enumerate(all_status):
                if status.status:
                    status.status = False
                    status.save()
                    self.lock.release()
                    return self.processors[index], status
            self.lock.release()

            # all processors are currently busy
            # wait 3 sec before finding a new idle processor/worker again
            print("all workers are currently occupied.\n")
            print("system will automatically find a new worker again in 3 sec...\n")
            time.sleep(3)

        # timeout
        return None, None

    def read_config(self):
        f = open(self.CONFIG_FILE_NAME, "r")
        data = f.read().split("\n")
        data = data[:-1]
        workers_address = []
        for addr in data:
            ip = addr.split(" ")[0]
            port = int(addr.split(" ")[1])
            workers_address.append((ip, port))
        return workers_address

