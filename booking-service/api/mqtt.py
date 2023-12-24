import paho.mqtt.client as mqtt

mqtt_client = mqtt.Client(client_id="booking-service", clean_session=True, protocol=mqtt.MQTTv311)
mqtt_client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        mqtt_client.subscribe("acknowledgment")
    else:
        print("Connection failed with code " + str(rc))


mqtt_client.on_connect = on_connect
mqtt_client.username_pw_set("group7", "Group777")