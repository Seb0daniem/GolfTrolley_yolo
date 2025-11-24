### IMPORTS ###
import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic} | Message: {msg.payload.decode()}")

def main():
    client = mqtt.Client()
    client.on_message = on_message

    client.connect("localhost", 1883)
    client.subscribe("inference_metadata")

    print("Listening for messages...")
    client.loop_forever()

if __name__ == "__main__":
    main()
