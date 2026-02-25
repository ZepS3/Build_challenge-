import threading
import time
import random

class Consumer(threading.Thread):
    def __init__(self, shared_queue):
        super().__init__()
        self.shared_queue = shared_queue
        self.consumed_items = []
        self.stop_event = threading.Event()

    def run(self):
        print("[Consumer] Starting consumption...")
        while not self.stop_event.is_set():
            try:
                item = self.shared_queue.dequeue()
                if item is None:
                    print("[Consumer] Queue stopped. Exiting.")
                    break
                
                time.sleep(random.uniform(0.2, 0.6))
                self.consumed_items.append(item)
                print(f"[Consumer] Processed: {item}")
            except Exception as e:
                print(f"[Consumer] Error: {e}")
                break
        
        print(f"[Consumer] Consumption finished. Total processed: {len(self.consumed_items)}")

    def stop(self):
        self.stop_event.set()
