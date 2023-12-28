import json
from .mqtt import mqtt_client
import time


# Global variable to store the acknowledgment status
acknowledgment_received = None
acknowledgment_topic = "acknowledgment"

def publishMessage(topic,payload):

    try:
        mqtt_client.publish(topic, json.dumps(payload),1)
        return None
    except Exception as e:
        return json({'error': str(e)}), 500


# Callback to handle incoming MQTT messages
def on_message(client, userdata, msg):
    global acknowledgment_received
    try:
        payload = json.loads(msg.payload)
        print("Payload:", payload)
        json_payload = json.loads(payload)
        print(json_payload)
        acknowledgment_received = json_payload
       
    except json.JSONDecodeError as e:
        print(f"Error decoding MQTT message payload: {e}")


# Function to subscribe and wait for acknowledgment
def wait_for_acknowledgment(correlation_id):
    global acknowledgment_received
    acknowledgment_received = None

    # Subscribe to the acknowledgment topic
    mqtt_client.subscribe(acknowledgment_topic)

    # Wait for acknowledgment or timeout
    start_time = time.time()
    timeout = 10 

    while acknowledgment_received is None and time.time() - start_time < timeout:
        time.sleep(1.0)

    # Unsubscribe from the acknowledgment topic
    mqtt_client.unsubscribe(acknowledgment_topic)

    if acknowledgment_received is None:
        return False
    if acknowledgment_received['acknowledgment'] == 'True' and acknowledgment_received['correlation_id'] == str(correlation_id):
        return True
    else :
        return False


mqtt_client.on_message = on_message
