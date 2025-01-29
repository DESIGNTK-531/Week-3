# publisher.py
import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
    else:
        print(f"Connection failed with code {rc}")

# Create publisher client
publisher = mqtt.Client()
publisher.on_connect = on_connect

# Connect to public broker
print("Connecting to broker...")
publisher.connect("test.mosquitto.org", 1883, 60)
publisher.loop_start()

# Simulated agricultural sensors with realistic ranges
sensors = {
    "soil_moisture": {
        "location": "Field A - Tomatoes",
        "range": (20, 80),  # percentage
        "unit": "%",
        "optimal_range": (50, 65)
    },
    "soil_ph": {
        "location": "Field B - Lettuce",
        "range": (5.0, 7.5),  # pH scale
        "unit": "pH",
        "optimal_range": (6.0, 7.0)
    },
    "light_intensity": {
        "location": "Greenhouse 1",
        "range": (0, 100000),  # lux
        "unit": "lux",
        "optimal_range": (30000, 80000)
    },
    "temperature": {
        "location": "Field C - Peppers",
        "range": (10, 40),  # celsius
        "unit": "°C",
        "optimal_range": (20, 30)
    },
    "humidity": {
        "location": "Greenhouse 2",
        "range": (30, 90),  # percentage
        "unit": "%",
        "optimal_range": (60, 80)
    }
}

try:
    while True:
        # Select a random sensor
        sensor_type = random.choice(list(sensors.keys()))
        sensor_info = sensors[sensor_type]
        
        # Generate realistic sensor reading
        reading = random.uniform(*sensor_info["range"])
        
        # Create sensor data payload
        payload = {
            "type": sensor_type,
            "value": round(reading, 2),
            "unit": sensor_info["unit"],
            "location": sensor_info["location"],
            "optimal_range": sensor_info["optimal_range"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Publish to topic
        topic = "smartfarm/sensors/readings"
        publisher.publish(
            topic,
            json.dumps(payload),
            qos=1
        )
        print(f"🌱 Published {sensor_type} reading: {payload['value']} {payload['unit']}")
        time.sleep(10)
        
except KeyboardInterrupt:
    print("Stopping farm monitoring...")
    publisher.loop_stop()
    publisher.disconnect()