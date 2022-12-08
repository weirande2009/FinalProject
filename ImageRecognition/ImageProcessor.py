import socket
import numpy as np
import cv2


class ImageProcessor:
    """
    Image processor which connect to the remote worker
    """
    busy = None
    BUFFER_SIZE = 1024
    DATA_SIZE_LENGTH = 16

    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.sock = None
        # whether the processor is working
        self.busy = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def connect(self):
        """
        Connect to the remote worker
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))

    def recognize(self, img) -> str:
        """
        Recognize the given image
        :param img: image
        :return: the class name of the image
        """

        # Convert image into numpy
        # image = cv2.imdecode(np.frombuffer(img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        image = self.save_file(img)
        # Convert image to string
        data = image.tostring()
        # Send image
        self.busy = True
        # send height
        self.send(str(image.shape[0]).encode())
        # send width
        self.send(str(image.shape[1]).encode())
        self.send(data)
        # Receive result
        result = self.receive_all(-1).decode()
        self.busy = False
        return result

    def save_file(self, img):
        image = cv2.imread(img)
        return image

    def close(self):
        """
        close the connection to worker
        """
        self.sock.close()

    def receive_all(self, length=-1):
        """
        Receive all data from worker
        :param length: bytes number
        :return: the received data
        """
        if length == -1:
            length = int(self.receive_all(self.DATA_SIZE_LENGTH))
        buf = b''
        while length:
            new_buf = self.sock.recv(length)
            if not new_buf:
                return None
            buf += new_buf
            length -= len(new_buf)
        return buf

    def send(self, data: bytes):
        self.sock.send(str(len(data)).ljust(self.DATA_SIZE_LENGTH).encode())
        self.sock.send(data)
