class Item:
    def __init__(self, id, data, timestamp):
        self.id = id
        self.data = data
        self.timestamp = timestamp

    def __str__(self):
        return f"Item(id={self.id}, data='{self.data}')"
