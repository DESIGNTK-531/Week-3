import paho.mqtt.client as mqtt
import time
import openai
from openai import OpenAI
import json
from PIL import Image
import requests
from io import BytesIO

# Set your OpenAI API key
api_key = "<your-api-key>"

client = OpenAI(api_key=api_key)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to broker")
        client.subscribe("smartfarm/sensors/readings")
    else:
        print(f"Connection failed with code {rc}")
        


def analyze_farm_data(sensor_data):
    """
    Analyze farm sensor data and provide agricultural recommendations.
    """
    try:
        # Check if reading is within optimal range
        value = sensor_data['value']
        min_optimal, max_optimal = sensor_data['optimal_range']
        status = "optimal" if min_optimal <= value <= max_optimal else "suboptimal"
        
        prompt = f"""
        As a Smart Agriculture AI Advisor, analyze this sensor reading and provide a specific, 
        actionable recommendation (in one sentence):
        
        Sensor Type: {sensor_data['type']}
        Reading: {sensor_data['value']} {sensor_data['unit']}
        Location: {sensor_data['location']}
        Status: {status}
        Optimal Range: {min_optimal} to {max_optimal} {sensor_data['unit']}
        Time: {sensor_data['timestamp']}
        """
        
        # Get text recommendation
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        recommendation = response.choices[0].message.content

        # Generate image based on the recommendation
        image_prompt = f"Agricultural scene showing: {recommendation}"
        image_response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get the image URL
        image_url = image_response.data[0].url
        
        # Download and display the image
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.show()  # This will open the image in your default image viewer
        
        return recommendation, status
    except Exception as e:
        print(f"Error interacting with OpenAI: {e}")
        return "Error: Unable to process your request.", "error"

def on_message(client, userdata, msg):
    try:
        sensor_data = json.loads(msg.payload.decode())
        
        # Get AI analysis and status
        insight, status = analyze_farm_data(sensor_data)
        
        # Status emoji
        status_emoji = {
            "optimal": "✅",
            "suboptimal": "⚠️",
            "error": "❌"
        }
        
        # Print formatted output
        print("\n" + "🚜 " + "="*50 + " 🚜")
        print(f"📍 Location: {sensor_data['location']}")
        print(f"📊 {sensor_data['type'].replace('_', ' ').title()}: "
              f"{sensor_data['value']} {sensor_data['unit']} {status_emoji[status]}")
        print(f"📈 Optimal Range: {sensor_data['optimal_range'][0]} - "
              f"{sensor_data['optimal_range'][1]} {sensor_data['unit']}")
        print(f"🤖 AI Recommendation: {insight}")
        print("🚜 " + "="*50 + " 🚜\n")
        
    except json.JSONDecodeError:
        print("Failed to decode JSON payload")

# Create subscriber client
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

# Connect to public broker
print("Starting Smart Farm Monitoring System...")
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