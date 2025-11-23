from inference.run_inference import main as run_inference
from mqtt.publisher import MqttPublisher

def main():
    print("Hello from main.py")
    run_inference()

if __name__ == "__main__":
    main()
