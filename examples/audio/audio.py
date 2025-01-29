import base64
import json
import time
import pygame
import paho.mqtt.client as mqtt
from openai import OpenAI

# Initialize OpenAI client
api_key = "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"
client = OpenAI(api_key=api_key)

# Initialize pygame mixer
pygame.mixer.init()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        client.subscribe("smartfarm/sensors/readings")
    else:
        print(f"Connection failed with code {rc}")

def analyze_and_speak(sensor_data):
    try:
        # Check if reading is within optimal range
        value = sensor_data['value']
        min_optimal, max_optimal = sensor_data['optimal_range']
        status = "optimal" if min_optimal <= value <= max_optimal else "suboptimal"
        
        # Create message for text-to-speech
        message = f"""
        As a Smart Agriculture AI Advisor, analyze this sensor reading and provide a specific, 
        actionable recommendation (in one sentence):
        
        Sensor reading from {sensor_data['location']}: {value} {sensor_data['unit']}. Status is {status}.
        """
        
        # Generate audio using OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            messages=[{"role": "user", "content": message}]
        )

        # Save and play audio
        wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
        with open("sensor_reading.wav", "wb") as f:
            f.write(wav_bytes)

        # Play the audio file
        pygame.mixer.music.load("sensor_reading.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait for audio to finish playing
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(f"Error processing message: {e}")

def on_message(client, userdata, msg):
    try:
        sensor_data = json.loads(msg.payload.decode())
        analyze_and_speak(sensor_data)
        
    except json.JSONDecodeError:
        print("Failed to decode JSON payload")

# Create subscriber client
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

# Connect to public broker
print("Starting Smart Farm Audio Monitoring System...")
subscriber.connect("test.mosquitto.org", 1883, 60)

# Start the subscriber loop
subscriber.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Shutting down farm monitoring system...")
    subscriber.loop_stop()
    subscriber.disconnect()