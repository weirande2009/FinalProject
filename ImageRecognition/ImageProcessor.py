import socket
import cv2
import struct


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
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        # Convert image to string
        data = image.tostring()
        # Send image
        self.send(data)
        # Receive result
        result = self.receive_all().decode()
        print(result)
        return result

    def save_file(self, img):
        image = cv2.imread(img)
        return image

    def close(self):
        """
        close the connection to worker
        """
        self.sock.close()

    def receive_all(self):
        """
        Receive all data from worker
        :return: the received data
        """
        buf = b''
        l = struct.calcsize('!i')
        while l > 0:
            buf += self.sock.recv(l)
            l -= len(buf)
        length = struct.unpack('!i', buf[:4])[0]
        print("Length:", buf)
        received_length = 0
        print("Expected length:", length)
        buf = b''
        while length:
            new_buf = self.sock.recv(length)
            if not new_buf:
                return None
            buf += new_buf
            length -= len(new_buf)
            received_length += len(new_buf)
        print("Received length:", received_length)
        print("Data:", buf)
        return buf

    def send(self, data: bytes):
        val = struct.pack('!i', len(data))
        print(val)
        self.sock.send(val)
        self.sock.send(data)
