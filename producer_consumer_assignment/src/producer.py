import threading
import time
import random
from .item import Item

class Producer(threading.Thread):
    def __init__(self, shared_queue, item_count=20):
        super().__init__()
        self.shared_queue = shared_queue
        self.item_count = item_count
        self.stop_event = threading.Event()

    def run(self):
        print(f"[Producer] Starting production of {self.item_count} items...")
        for i in range(1, self.item_count + 1):
            if self.stop_event.is_set():
                break
            
            item = Item(i, f"Data-{i}")
            try:
                time.sleep(random.uniform(0.1, 0.5))
                self.shared_queue.enqueue(item)
                print(f"[Producer] Produced: {item}")
            except Exception as e:
                print(f"[Producer] Error: {e}")
                break
        
        print("[Producer] Production completed. Signaling stop.")
        self.shared_queue.stop()

    def stop(self):
        self.stop_event.set()
