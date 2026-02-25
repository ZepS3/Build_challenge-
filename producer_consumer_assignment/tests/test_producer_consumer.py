import unittest
import threading
import time
from src.shared_queue import SharedQueue
from src.item import Item
from src.producer import Producer
from src.consumer import Consumer

class TestProducerConsumer(unittest.TestCase):
    
    def setUp(self):
        self.queue = SharedQueue(capacity=2)

    def test_queue_enqueue_dequeue(self):
        item = Item(1, "Test Data")
        self.queue.enqueue(item)
        self.assertEqual(len(self.queue.queue), 1)
        
        dequeued = self.queue.dequeue()
        self.assertEqual(dequeued.id, 1)
        self.assertEqual(len(self.queue.queue), 0)

    def test_queue_capacity(self):
        # Fill the queue
        self.queue.enqueue(Item(1, "Data 1"))
        self.queue.enqueue(Item(2, "Data 2"))
        
        # Try to enqueue another item in a separate thread (it should block)
        def try_enqueue():
            self.queue.enqueue(Item(3, "Data 3"))
            
        t = threading.Thread(target=try_enqueue)
        t.start()
        
        time.sleep(0.1) # Give thread time to start and block
        self.assertTrue(t.is_alive()) # Should still be waiting
        
        # Consume one to make space
        self.queue.dequeue()
        time.sleep(0.1)
        
        # Now the thread should have finished enqueuing
        t.join(timeout=1)
        self.assertFalse(t.is_alive())
        self.assertEqual(len(self.queue.queue), 2) # 2 items left (2 and 3)

    def test_producer_consumer_integration(self):
        producer = Producer(self.queue, item_count=5)
        consumer = Consumer(self.queue)
        
        producer.start()
        consumer.start()
        
        producer.join()
        consumer.join()
        
        self.assertEqual(len(consumer.consumed_items), 5)
        self.assertEqual(len(self.queue.queue), 0)

if __name__ == '__main__':
    unittest.main()
