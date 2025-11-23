import paho.mqtt.client as mqtt

class MqttPublisher:
    def __init__(self, broker="172.17.0.1", port=1883, topic="inference_metadata"):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.topic = topic

    def publish(self, message: str):
        self.client.publish(self.topic, message)
