import time

class Item:
    def __init__(self, item_id, data):
        self.id = item_id
        self.data = data
        self.timestamp = time.time()

    def __str__(self):
        return f"Item(id={self.id}, data='{self.data}')"
