### IMPORTS ###
import paho.mqtt.client as mqtt

class MqttSubscriber:
    def __init__(self, topic="inference_metadata", host="localhost", port=1883):
        self.topic = topic
        self.host = host
        self.port = port
        self.received_data = None  # This will store the latest received message

        # Create the MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the MQTT broker
        self.client.connect(self.host, self.port)

        # Start a separate thread to listen for messages
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """Callback that runs when the client connects to the broker."""
        print(f"Connected to MQTT broker at {self.host}:{self.port} with result code {rc}")
        # Subscribe to the specified topic
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        """Callback that runs when a message is received."""
        self.received_data = msg.payload.decode()  # Save the received message

    def get_data(self):
        """Expose the latest data for other modules."""
        return self.received_data


if __name__ == "__main__":
    subscriber = MqttSubscriber()
    try:
        while True:
            # Keep the program running and display the latest message
            if subscriber.get_data():
                print(f"Latest data: {subscriber.get_data()}")
    except KeyboardInterrupt:
        print("Shutting down...")
        subscriber.client.loop_stop()
        subscriber.client.disconnect()
