# ESP32 Web Controller — Project Documentation

## Overview

This project uses an **ESP32 board** as a local web server to remotely control peripherals via Wi-Fi.  
It provides a simple **web interface** to manage the following devices:

- **NeoPixel LED strip** (color & count)
- **Buzzer** (single beeps, musical notes & melodies)
- **OLED screen** (custom messages & status display)
- **DHT11 sensor** (temperature & humidity)

All interactions are done wirelessly through a browser by connecting to the ESP32’s Wi-Fi access point.

---

## Wi-Fi Access Point

The ESP32 acts as a Wi-Fi access point with the following credentials:

- **SSID**: `ESP32 Wifi`
- **Password**: `123456789`

Once connected, you can access the web interface at:  
`http://192.168.4.1`

---

## Web Interface Features

### 1. LED Control

- **Color sliders** allow you to set the RGB values (0–255) of the NeoPixel LED strip.
- **LED count selector** lets you choose how many of the 12 LEDs should light up with the selected color.

---

### 2. Buzzer & Music

- **"Beep Beep" button** triggers two short consecutive beeps at 500 Hz.
- **Musical Notes**: Play individual notes (C4 to C5) with a button interface using PWM control.
- **Melody Playback** (optional):
  - A text field allows entering a number between 0 and 41 to play a predefined melody using the `playsong(melody[x])` function.

---

### 3. OLED Display

- A text field allows displaying a custom message (max ~20 characters) on the OLED screen.
- The OLED also shows feedback/status messages for every action performed (color change, note played, etc.).

---

### 4. DHT11 Temperature Sensor

- A dedicated button lets you measure and display:
  - Temperature (in °C)
  - Humidity (in %)
- The data is shown on both the webpage and the OLED screen.

---

## Technologies Used

- **MicroPython**
- **Microdot** (for lightweight web server)
- **NeoPixel** (WS2812 LEDs)
- **PWM** (for buzzer audio output)
- **SSD1306** OLED display (via I2C)
- **DHT11** temperature & humidity sensor

---

## Status Feedback System
Every user action updates a "Status" section on the web page, and the same message is displayed on the OLED screen for instant feedback.

Example messages:

- Color updated
- LED count updated
- Note played: A4
- Temperature: 23°C | Humidity: 60%

---

Creator : HELL Maxime
