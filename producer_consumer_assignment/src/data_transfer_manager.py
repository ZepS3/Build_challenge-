from .producer import Producer
from .consumer import Consumer
from .shared_queue import SharedQueue

class DataTransferManager:
    def __init__(self, capacity=5, item_count=20):
        self.shared_queue = SharedQueue(capacity=capacity)
        self.producer = Producer(self.shared_queue, item_count=item_count)
        self.consumer = Consumer(self.shared_queue)

    def start_transfer(self):
        self.producer.start()
        self.consumer.start()

    def stop_transfer(self):
        self.producer.stop()
        self.consumer.stop()
        self.shared_queue.stop()

    def wait_for_completion(self):
        self.producer.join()
        self.consumer.join()
        print("All threads have completed.")
