from inference.run_inference import InferenceRunner
from mqtt.publisher import MqttPublisher

def main():
    publisher = MqttPublisher()

    model = "yolo11s"
    source = 0
    #source = "https://www.youtube.com/watch?v=SeRUThVhlc4"
    model_path = "inference/models/" + model + ".engine"

    inference = InferenceRunner(
        model_path=model_path,
        publisher=publisher,
        source=source,
        conf=None,
        classes=None)
    inference.run()



if __name__ == "__main__":
    main()
