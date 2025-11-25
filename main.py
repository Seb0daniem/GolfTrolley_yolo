from inference.run_inference import main as run_inference
import threading

def main():
    print("Hello from main.py")
    
    # Create threads for parallel execution
    inference_thread = threading.Thread(target=run_inference, daemon=True)
    
    # Start thread
    inference_thread.start()
    
    # Keep main thread alive
    try:
        inference_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
