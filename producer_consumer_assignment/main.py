from src.data_transfer_manager import DataTransferManager
import time

def main():
    print("=== Producer-Consumer Data Transfer System ===")
    
    # Create manager with capacity 5 and count 10
    manager = DataTransferManager(capacity=5, item_count=10)
    
    try:
        print("\n[System] Starting transfer...")
        manager.start_transfer()
        
        # Wait for threads to complete
        manager.wait_for_completion()
        
    except KeyboardInterrupt:
        print("\n[System] Interrupted by user. stopping...")
        manager.stop_transfer()
    
    print("\n[System] Transfer process finished.")

if __name__ == "__main__":
    main()
