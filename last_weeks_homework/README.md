# Smart Agriculture IoT Monitoring System

## Overview
This project simulates a smart agriculture monitoring system using MQTT protocol and AI-powered insights. The system monitors various environmental parameters crucial for crop health and provides real-time recommendations for optimal farming conditions.

Features
- Real-time monitoring of:
  - Soil moisture levels
  - Soil pH
  - Light intensity
  - Temperature
  - Humidity
- AI-powered analysis and recommendations
- Multiple location/crop monitoring
- Optimal range checking and status indicators


## Prerequisites
- Python 3.8 or higher
- Internet connection for MQTT broker and OpenAI API

## Installation
1. Clone the repository

```
git clone https://github.com/your-repo/smart-agriculture-iot.git
```

2. Install the required Python packages

```
pip install paho-mqtt openai
```

## Running the Application

1. Start the subscriber (monitoring system)

```
python sub.py
```

2. In a separate terminal, start the publisher (simulating sensor readings)

```
python pub.py
```

## How It Works
Publisher (pub.py) s
- Simulates various agricultural sensors
- Generates realistic sensor readings within defined ranges
- Publishes sensor data to the MQTT broker every 5 seconds
- Includes metadata like location, timestamp, and optimal range

Subscriber (sub.py) 
- Receives sensor data from the MQTT broker
- Analyzes the data using OpenAI's GPT-4o model
- Provides real-time recommendations for optimal farming conditions
- Displays the analysis in a formatted message

## Sample Output
```
🚜 ================================================== 🚜
📍 Location: Greenhouse 1
📊 Light Intensity: 25000 lux ⚠️
📈 Optimal Range: 30000 - 80000 lux
🤖 AI Recommendation: Consider removing shade cloths or adjusting grow lights to increase light intensity for optimal plant growth.
🚜 ================================================== 🚜
```