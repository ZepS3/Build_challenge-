import time
from src.data_transfer_manager import DataTransferManager
from src.item import Item

def main():
    print("=== Producer-Consumer Data Transfer System ===")
    
    source_items = [Item(i, f"Data-{i}", time.time()) for i in range(1, 11)]
    destination_items = []
    
    manager = DataTransferManager(source_items, destination_items, capacity=10)
    
    try:
        print("\n[System] Starting transfer...")
        manager.startTransfer()
        
        manager.waitForCompletion()
        
    except KeyboardInterrupt:
        print("\n[System] Interrupted by user. stopping...")
        manager.stopTransfer()
    
    print(f"\n[System] Transfer process finished. Processed {len(destination_items)} items.")

if __name__ == "__main__":
    main()