import threading
from .producer import Producer
from .consumer import Consumer
from .shared_queue import SharedQueue

class DataTransferManager:
    def __init__(self, sourceContainer, destinationContainer, capacity=10):
        self.lock = threading.Lock()
        self.shared_queue = SharedQueue(capacity=capacity, lock=self.lock)
        self.producer = Producer(sourceContainer, self.shared_queue)
        self.consumer = Consumer(self.shared_queue, destinationContainer)

    def startTransfer(self):
        self.producer.start()
        self.consumer.start()

    def stopTransfer(self):
        self.producer.stop()
        self.consumer.stop()
        self.shared_queue.stop()

    def waitForCompletion(self):
        self.producer.join()
        self.shared_queue.stop() 
        self.consumer.join()
        print("Transfer completed.")