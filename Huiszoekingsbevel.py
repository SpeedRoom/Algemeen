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
from paho.mqtt import client as mqtt_client

# MQTT stuff
broker = '192.168.0.190'  #IP-adres rpi
port = 1883  
topic_tetris = "esp_tetris/output"
topic_doolhof = "esp_doolhof/output"
client_id = "rp" 
username = 'sienp' 
password = 'sienp'  

message_tetris = ""
message_doolhof = ""

WIE = "a"
WAAR = "b"
WANNEER = "c"
MAX = 5

global pogingen
pogingen =0

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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic == "esp_doolhof/output":
            message_doolhof = msg.payload.decode()
        if msg.topic == "esp_tetris/output":
            message_tetris = msg.payload.decode()

    client.subscribe(topic_tetris, topic_doolhof)
    client.on_message = on_message


def controleer(wie, waar, wanneer):
    global pogingen
    if pogingen < MAX:
        verzend_button.enable()
    else:
        app.error(title="Maximum aantal aanvragen overschreden", text=error_message)
        time.sleep(600)  # 600 seconden (=10min) wachten (vevangen door iets anders, want nu freezed hij gewoon)
        verzend_button.enable()
    if wie==WIE and waar==WAAR and wanneer==WANNEER:
        print_bevel()
        app.info(title="Huiszoeking goedgekeurd", text=bevel)
        return
    else:
        error()
    return

def print_bevel():  # Hier commando geven aan printer om te printen + "deur" open
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
    return wie, waar, wanneer


if __name__ == '__main__':


    app = App(title="Huiszoekingsbevel", height=320, width=480, layout="grid")  # creates schermvakje van de grootte van het TFT shield
    
    name_label = Text(app, text="Naam van de verdachte: ", grid=[0,0],  font="Cambria")
    name = TextBox(app, grid=[1,0], text="Voornaam Naam", width="fill", enabled=False)
    address_label = Text(app, text="Adres van de misdaad: ", grid=[0,1], font="Cambria")
    address = TextBox(app, grid=[1,1], text="Gebroeders Desmetstraat 1, 9000 Gent", width="fill")
    date_label = Text(app, text="Datum van de misdaad: ", grid=[0,2], font="Cambria")
    date = TextBox(app, grid=[1,2], text="dd/mm/jjjj", width="fill", enabled=False)
    verzend_button = PushButton(app, text="Verzend", command=verzend, grid=[1,3], width="fill")


    client = connect_mqtt()
    subscribe(client)
    client.loop_start()  
    
    #controle van de ontvangen berichten
    if message_doolhof == WANNEER:
        date = TextBox(app, grid=[1,2], text=message_doolhof, width="fill", enabled=False)
        
    if message_tetris == "voltooid":
        name = TextBox(app, grid=[1,0], text="Voornaam Naam", width="fill", enabled=True)
    else:
        name = TextBox(app, grid=[1,0], text="Voornaam Naam", width="fill", enabled=False)

    app.display()
