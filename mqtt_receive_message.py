import paho.mqtt.client as mqtt
import ssl

# HiveMQ Cloud dane
MQTT_BROKER = "xxx"
MQTT_PORT = 8883
MQTT_TOPIC = "test/esp32/random"
MQTT_USER = "xxx"
MQTT_PASSWORD = "xxx" 

def on_connect(client, rc):
    if rc == 0:
        print("Połączono z MQTT")
        client.subscribe(MQTT_TOPIC)
        print(f"Zasubskrybowano temat: {MQTT_TOPIC}")
    else:
        print(f"Błąd, kod: {rc}")

def on_message(msg):
    print(f"Odebrano wiadomość: {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_forever()
