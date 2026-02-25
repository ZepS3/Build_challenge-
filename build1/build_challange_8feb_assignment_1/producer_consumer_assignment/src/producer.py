import threading
import time
import random

class Producer(threading.Thread):
    def __init__(self, sourceContainer, sharedQueue):
        super().__init__()
        self.sourceContainer = sourceContainer
        self.sharedQueue = sharedQueue
        self.stop_event = threading.Event()

    def run(self):
        for item in self.sourceContainer:
            if self.stop_event.is_set():
                break
            
            try:
                time.sleep(random.uniform(0.1, 0.5))
                self.sharedQueue.enqueue(item)
                print(f"[Producer] Produced: {item}")
            except Exception as e:
                print(f"[Producer] Error: {e}")
                break
        
        print("[Producer] Production completed.")

    def stop(self):
        self.stop_event.set()