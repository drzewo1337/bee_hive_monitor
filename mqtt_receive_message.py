import paho.mqtt.client as mqtt
import ssl

# HiveMQ Cloud dane
MQTT_BROKER = "xxx"
MQTT_PORT = 8883
MQTT_TOPIC = "test/esp32/random"
MQTT_USER = "xxx"
MQTT_PASSWORD = "xxx" 

# Callback — po połączeniu
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Połączono z MQTT brokerem!")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Subskrybowano temat: {MQTT_TOPIC}")
    else:
        print(f"❌ Błąd połączenia. Kod: {rc}")

# Callback — po odebraniu wiadomości
def on_message(client, userdata, msg):
    print(f"📩 Odebrano wiadomość: {msg.topic} -> {msg.payload.decode()}")

# Konfiguracja klienta
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)

client.on_connect = on_connect
client.on_message = on_message

# Połączenie z brokerem
client.connect(MQTT_BROKER, MQTT_PORT)

# Start loop
client.loop_forever()
