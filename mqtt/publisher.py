import paho.mqtt.client as mqtt

class MqttPublisher:
    def __init__(self, broker="host.docker.internal", port=1883, topic="inference_metadata"):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        self.topic = topic

    def publish(self, message: str):
        self.client.publish(self.topic, message)
