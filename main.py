from inference.run_inference import InferenceRunner
from mqtt.publisher import MqttPublisher

def main():
    publisher = MqttPublisher()

    model = "yolo11l"
    source = 0
    model_path = "inference/models/" + model + ".engine"

    inference = InferenceRunner(model_path=model_path, publisher=publisher, source=source)
    inference.run()



if __name__ == "__main__":
    main()
