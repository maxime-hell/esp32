from microdot import Microdot, Response
import network
import time
from neopixel import NeoPixel
from machine import Pin
from machine import PWM, Pin # Added for the pin of buzzer
from utime import sleep	# Added for the time managment of buzzer
from machine import I2C, RTC # Added for the Oled screen
import ssd1306 # Added for the Oled screen
import dht # Added for dht11 sensor

# Config Wi-Fi
Name = "ESP32 Wifi"
Password = "123456789"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=Name, password=Password, authmode=3)

while not ap.active():
    print("Creating access point...")
    time.sleep(0.5)
print("Access Point created:", ap.ifconfig())

# LED Strip
led_strip = NeoPixel(Pin(23), 12)

current = 12
r = 0
g = 0
b = 0

def turn_on_LEDs():
    for i in range(12):
        if i < current:
            led_strip[i] = (r, g, b)
        else:
            led_strip[i] = (0, 0, 0)
    led_strip.write()
    
def display_status_on_oled(msg):
    oled.fill(0)
    oled.text(msg[:16], 0, 0)
    oled.show()

# Buzzer managment
buzzer_pwm = PWM(Pin(14))
buzzer_pwm.duty_u16(0)
notes_freq = {
    "C4": 262,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
}

# OLED managment
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Dht11 sensor managment
tmp = dht.DHT11(Pin(27))

# Web Server
app = Microdot()
Response.default_content_type = 'text/html'

html_site = """<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 WEB</title>
</head>
<body>
    <h1>ESP32 Control</h1>
    <p>Status: {status}</p>
    
    <h3>LED control</h3>
    <form action="/color" method="get">
        <h4>Change color</h4>
        <label for="r" style="color: red;">RED:</label>
        <input type="range" name="r" min="0" max="255" value="0"><br>
        <label for="g" style="color: green;">GREEN:</label>
        <input type="range" name="g" min="0" max="255" value="0"><br>
        <label for="b" style="color: blue;">BLUE:</label>
        <input type="range" name="b" min="0" max="255" value="0"><br>
        <input type="submit" value="Set Color">
    </form>
    
    <form action="/count" method="get">
        <h4>Change LED count</h4>
        <input type="number" name="n" min="0" max="12" value="12">
        <input type="submit" value="Update">
    </form>
    
    <h3>Play notes</h3>
    <form action="/beepbeep" method="get" style="margin-bottom: 10px;">
        <input type="submit" value="Beep Beep!">
    </form>
    <form action="/note" method="get">
        <div>
            <button name="n" value="C4">Do (C)</button>
            <button name="n" value="D4">Ré (D)</button>
            <button name="n" value="E4">Mi (E)</button>
            <button name="n" value="F4">Fa (F)</button>
        </div>
        <div>
            <button name="n" value="G4">Sol (G)</button>
            <button name="n" value="A4">La (A)</button>
            <button name="n" value="B4">Si (B)</button>
            <button name="n" value="C5">Do (C5)</button>
        </div>
    </form>
    
    <h3>OLED display</h3>
    <form action="/oled" method="get">
        <input type="text" name="msg" maxlength="20" placeholder="Message to display">
        <input type="submit" value="Display">
    </form>
    
    <h3>DHT11 sensor</h3>
    <form action="/temperature" method="get">
        <input type="submit" value="Measure Temperature">
    </form>
    
</body>
</html>"""


@app.route('/')
def home(request):
    try:
        tmp.measure()
        temperature = tmp.temperature()
        humidity = tmp.humidity()
        status = f"Temp: {temperature}°C | Hum: {humidity}%"
    except:
        status = "Erreur DHT11 sensor"

    return html_site.format(status=status), 200

@app.route('/color')
def set_color(request):
    global r, g, b
    try:
        r = int(request.args.get('r', 0))
        g = int(request.args.get('g', 0))
        b = int(request.args.get('b', 0))
    except:
        return html_site.format(status='Error parsing color values'), 200
    
    turn_on_LEDs()
    status='Color updated'
    display_status_on_oled(status)
    return html_site.format(status=status), 200

@app.route('/count')
def set_count(request):
    global current
    try:
        current = int(request.args.get('n', 12))
    except:
        return html_site.format(status='Error parsing count'), 200

    turn_on_LEDs()
    status='LED count updated'
    display_status_on_oled(status)
    return html_site.format(status=status), 200

@app.route('/beepbeep')
def beepbeep(request):
    for _ in range(2):
        buzzer_pwm.freq(500)
        buzzer_pwm.duty_u16(32768)
        sleep(0.15)
        buzzer_pwm.duty_u16(0)
        sleep(0.1)
        
    status='Beep beep played'
    display_status_on_oled(status)
    return html_site.format(status=status), 200

@app.route('/note')
def play_note(request):
    note = request.args.get('n')

    if note in notes_freq:
        freq = notes_freq[note]
        buzzer_pwm.freq(freq)
        buzzer_pwm.duty_u16(32768)
        sleep(0.3)
        buzzer_pwm.duty_u16(0)
        status = f"Note played : {note}"
    else:
        status = "Unknow note"
        
    display_status_on_oled(status)
    return html_site.format(status=status), 200

@app.route('/oled')
def display_oled(request):
    message = request.args.get('msg', '')

    oled.fill(0)
    oled.text(message, 0, 0)
    oled.show()

    return html_site.format(status=f"Display message : {message}"), 200

@app.route('/temperature')
def temperature(request):
    try:
        tmp.measure()
        temperature = tmp.temperature()
        humidity = tmp.humidity()
        status = f"Temperature : {temperature}°C | Humidity : {humidity}%"

        # Displaying on OLED screen
        oled.fill(0)
        oled.text(f"Temp: {temperature}C", 0, 0)
        oled.text(f"Hum: {humidity}%", 0, 10)
        oled.show()
    except:
        status = "Erreur reading the sensor"
        oled.fill(0)
        oled.text("Sensor error", 0, 0)
        oled.show()

    return html_site.format(status=status), 200


# Server start
app.run(port=80, debug=True)
