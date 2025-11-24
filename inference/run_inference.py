### IMPORTS ###
from ultralytics import YOLO
from mqtt.publisher import MqttPublisher


### CODE ###

def main():
    print("Hello from run_inference.py")
    publisher = MqttPublisher()

    # Load model
    model = YOLO("inference/models/yolo11s.engine")

    # For saving video, recorded and videos will become folders
    project = "recorded"
    name = "videos"

    # Run prediction on an image
    results = model.track(
        source=0,
        conf=0.7,
        save=True,
        stream=True,
        show=True,
        classes=0,
        project=project,
        name=name,
    )

    # Print results
    for r in results:
        #print(f"Results: {r}")
        # Publish inference metadata
        publisher.publish(str(r.boxes))

if __name__ == "__main__":
    main()