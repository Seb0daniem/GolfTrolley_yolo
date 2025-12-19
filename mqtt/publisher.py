### IMPORTS ###
import paho.mqtt.client as mqtt


class MqttPublisher:
    def __init__(self, broker="localhost", port=1883, topic="inference_metadata"):
        self.client = mqtt.Client()
        self.client.connect(broker, port)
        print(f"✓ Connected to MQTT broker at {broker}:{port}")
        self.topic = topic

    def publish(self, message: str):
        self.client.publish(self.topic, message)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
        print("Publisher cleaned up.")
