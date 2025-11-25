### IMPORTS ###
from ultralytics import YOLO
from mqtt.publisher import MqttPublisher


def main():
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
        classes=0,
        project=project,
        name=name,
    )

    # Process results
    for result in results:
        for box in result.boxes:
            xyxy = [int(v) for v in box.xyxy[0].tolist()] # pixel coords
            obj_id = int(box.id[0]) if box.id is not None else -1
            conf = round(float(box.conf[0]), 2)

            # Create MQTT-message
            message = {
                "id": obj_id,
                "conf": conf,
                "xyxy": xyxy,
            }

            publisher.publish(str(message))

if __name__ == "__main__":
    main()