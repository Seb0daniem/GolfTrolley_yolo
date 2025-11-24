from inference.run_inference import main as run_inference
from mqtt.subscriber import main as run_subscriber
import threading

def main():
    print("Hello from main.py")
    
    # Create threads for parallel execution
    inference_thread = threading.Thread(target=run_inference, daemon=True)
    subscriber_thread = threading.Thread(target=run_subscriber, daemon=True)
    
    # Start both threads
    inference_thread.start()
    subscriber_thread.start()
    
    print("✓ Inference and subscriber running in parallel")
    
    # Keep main thread alive
    try:
        inference_thread.join()
        subscriber_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
