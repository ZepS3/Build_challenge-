import threading
import time

class SharedQueue:
    """
    A thread-safe queue implementation using Condition variables.
    """
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.queue = []
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
        self.is_active = True

    def enqueue(self, item):
        """Add an item to the queue. Blocks if the queue is full."""
        with self.not_full:
            while len(self.queue) >= self.capacity and self.is_active:
                print(f"[Queue] Full. Waiting... (Size: {len(self.queue)})")
                self.not_full.wait()
            
            if not self.is_active:
                raise Exception("Queue has been stopped")

            self.queue.append(item)
            print(f"[Queue] Item {item.id} added. (Size: {len(self.queue)})")
            self.not_empty.notify()

    def dequeue(self):
        """Remove and return an item. Blocks if empty."""
        with self.not_empty:
            while len(self.queue) == 0 and self.is_active:
                print(f"[Queue] Queue is empty. Consumer waiting...")
                self.not_empty.wait()

            if len(self.queue) == 0 and not self.is_active:
                return None

            item = self.queue.pop(0)
            print(f"[Queue] Item {item.id} removed. (Size: {len(self.queue)})")
            self.not_full.notify()
            return item

    def stop(self):
        """
        Signals that no more items will be produced. Wakes up all waiting threads.
        """
        with self.lock:
            self.is_active = False
            self.not_empty.notify_all()
            self.not_full.notify_all()

    def get_stats(self):
        """
        Returns the current status of the queue.
        """
        with self.lock:
            return {
                "size": len(self.queue),
                "capacity": self.capacity,
                "is_active": self.is_active
            }
