import threading
import time
import random

class Consumer(threading.Thread):
    def __init__(self, sharedQueue, destinationContainer):
        super().__init__()
        self.sharedQueue = sharedQueue
        self.destinationContainer = destinationContainer
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            try:
                item = self.sharedQueue.dequeue()
                if item is None:
                    break
                
                time.sleep(random.uniform(0.2, 0.6))
                self.destinationContainer.append(item)
                print(f"[Consumer] Processed: {item}")
            except Exception as e:
                print(f"[Consumer] Error: {e}")
                break

    def stop(self):
        self.stop_event.set()