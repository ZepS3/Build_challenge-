import threading

class SharedQueue:
    def __init__(self, capacity, lock):
        self.capacity = capacity
        self.queue = []
        self.lock = lock
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
        self.is_active = True

    def enqueue(self, item):
        with self.not_full:
            while len(self.queue) >= self.capacity and self.is_active:
                success = self.not_full.wait(timeout=5.0)
                if not success:
                    raise Exception("Queue overflow timeout: Producer waited too long.")
            
            if not self.is_active:
                raise Exception("Queue has been stopped")

            self.queue.append(item)
            self.not_empty.notify()

    def dequeue(self):
        with self.not_empty:
            while len(self.queue) == 0 and self.is_active:
                success = self.not_empty.wait(timeout=5.0)
                if not success:
                    raise Exception("Queue empty timeout: Consumer waited too long.")

            if len(self.queue) == 0 and not self.is_active:
                return None

            item = self.queue.pop(0)
            self.not_full.notify()
            return item

    def stop(self):
        with self.lock:
            self.is_active = False
            self.not_empty.notify_all()
            self.not_full.notify_all()

    def getQueueStatus(self):
        with self.lock:
            return {
                "size": len(self.queue),
                "capacity": self.capacity,
                "is_active": self.is_active
            }