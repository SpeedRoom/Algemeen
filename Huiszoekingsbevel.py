"""
TODO
1. printer connecteren, file maken en toevoegen
2. WIE, WAAR en WANNEER kiezen
3. Delay of max aantal pogingen?
4. MQTT stuff nakijken en eventueel fiksen
"""

from guizero import *
import time
import random
import os
from paho.mqtt import client as mqtt_client
import cups


# conn = cups.Connection()
# printers = conn.getPrinters()
# printer_name = 'speedroom'


# MQTT stuff
broker = '192.168.1.61'  # IP-adres rpi
port = 1883  
topic_tetris = "esp_tetris/output"
topic_doolhof = "esp_doolhof/output"
topic_gsm = "esp_gsm/input"
client_id = "rp" 
username = 'sienp' 
password = 'sienp'  

WIE = "a"
WAAR = "b"
WANNEER = "c"
MAX = 5

pogingen = 0

weiger_message = "Uw aanvraag voor een huiszoeking is geweigerd. Controleer of alle gegevens juist gespeld zijn."
bevel = "Om aanvraag voor een huiszoeking is goedgekeurd. Uw huiszoekingsbevel wordt geprint."
error_message = "Het maximum aantal aanvragen voor huiszoeking is overschreden, probeer over 10 minuten nog eens."


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode('utf-8')}` from `{msg.topic}` topic")
        if msg.topic == "esp_doolhof/output":
            if str(msg.payload.decode('utf-8')) == WANNEER:
                date = TextBox(app, grid=[1, 2], text=str(msg.payload.decode('utf-8')), width="fill", enabled=False)
                print("date unlocked")

    client.subscribe([(topic_doolhof, 0), (topic_tetris, 0)])
    client.on_message = on_message


def controleer(wie, waar, wanneer):
    global pogingen
    if wie == WIE and waar == WAAR and wanneer == WANNEER:
        print_bevel()
        app.info(title="Huiszoeking goedgekeurd", text=bevel)
        return
    elif pogingen < MAX:
        error()
        verzend_button.enable()
    else:
        app.error(title="Maximum aantal aanvragen overschreden", text=error_message)
        time.sleep(300)  # 300 seconden (=5min) wachten (vevangen door iets anders, want nu freezed hij gewoon)
        pogingen = 0
        verzend_button.enable()
    return


def print_bevel():  # Hier commando geven aan printer om te printen + mqtt bevel om gsm's aan te steken : "open"
    os.system("lpr -P speedroom huiszoekingsbevel.pdf")  # printer name en file_name nog aanpassen, file bij in projectmap zetten
    #conn.printFile(printer_name,'/home/pi/Desktop/a.pdf',"",{}) 
    publish(client, topic_gsm, "open")
    return


def error():
    app.info(title="Huiszoeking geweigerd", text=weiger_message)
    return


def verzend():
    global pogingen
    print("Aanvraag huiszoeking is verstuurd.")
    verzend_button.disable()
    pogingen += 1
    wie = name.value
    waar = address.value
    wanneer = date.value
    controleer(wie, waar, wanneer)
    print(wie, waar, wanneer)
    os.system("lpr -P speedroom huiszoekingsbevel.pdf")
    #conn.printFile(printer_name,'huiszoekingsbevel.pdf',"",{}) 
    return wie, waar, wanneer


app = App(title="Huiszoekingsbevel", height=320, width=480, layout="grid")  # creates schermvakje van de grootte van het TFT shield
    
name_label = Text(app, text="Naam van de verdachte: ", grid=[0,0],  font="Cambria")
name = TextBox(app, grid=[1,0], text="Voornaam Naam", width="fill")
address_label = Text(app, text="Adres van de misdaad: ", grid=[0,1], font="Cambria")
address = TextBox(app, grid=[1,1], text="Gebroeders Desmetstraat 1, 9000 Gent", width="fill")
date_label = Text(app, text="Datum van de misdaad: ", grid=[0,2], font="Cambria")
date = TextBox(app, grid=[1,2], text="dd/mm/jjjj", width="fill", enabled=False)
verzend_button = PushButton(app, text="Verzend", command=verzend, grid=[1,3], width="fill")
picture = Picture(app, image="Justitie.png", align="bottom", grid=[1, 4])  #ook eens proberen zonder grid, eventueel nog met width


client = connect_mqtt()
subscribe(client)
client.loop_start()

app.display()

client.loop_stop()  # stopt pas als gui geclosed wordt
