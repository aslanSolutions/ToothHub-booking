import paho.mqtt.client as mqtt

broker_address = None
port = None

# Callback function to confirm connection with the broker
def on_connect(client, userdata, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
        print("User data: "+str(userdata))
        client.subscribe("topic/1")
        client.subscribe("topic/2")
        client.subscribe("topic/3")
    else:
        print("Connection failed with code "+str(rc))

# Callback function for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# Connection the client instance to the broker address and port
# and using the callback functions
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)
client.loop_forever()