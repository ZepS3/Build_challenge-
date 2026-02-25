import unittest
import threading
import time
from src.shared_queue import SharedQueue
from src.item import Item
from src.data_transfer_manager import DataTransferManager

class TestProducerConsumer(unittest.TestCase):
    
    def setUp(self):
        self.lock = threading.Lock()
        self.queue = SharedQueue(capacity=2, lock=self.lock)

    def test_queue_enqueue_dequeue(self):
        item = Item(1, "Test Data", time.time())
        self.queue.enqueue(item)
        self.assertEqual(len(self.queue.queue), 1)
        
        dequeued = self.queue.dequeue()
        self.assertEqual(dequeued.id, 1)
        self.assertEqual(len(self.queue.queue), 0)

    def test_queue_capacity_and_timeout(self):
        self.queue.enqueue(Item(1, "Data 1", time.time()))
        self.queue.enqueue(Item(2, "Data 2", time.time()))
        
        with self.assertRaises(Exception) as context:
            self.queue.enqueue(Item(3, "Data 3", time.time()))
        
        self.assertTrue("Queue overflow timeout" in str(context.exception))

    def test_producer_consumer_integration(self):
        source = [Item(i, f"Data-{i}", time.time()) for i in range(1, 6)]
        dest = []
        
        manager = DataTransferManager(source, dest, capacity=2)
        manager.startTransfer()
        manager.waitForCompletion()
        
        self.assertEqual(len(dest), 5)
        self.assertEqual(len(manager.shared_queue.queue), 0)

if __name__ == '__main__':
    unittest.main()