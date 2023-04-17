"""
TODO
1. printer connecteren, file maken en toevoegen
2. WIE, WAAR en WANNEER kiezen
3. Delay of max aantal pogingen?
"""

from guizero import *
import time

WIE = "a"
WAAR = "b"
WANNEER = "c"
MAX = 5
pogingen = 0

weiger_message = "Uw aanvraag voor een huiszoeking is geweigerd. Controleer of alle gegevens juist gespeld zijn."
bevel = "Om aanvraag voor een huiszoeking is goedgekeurd. Uw huiszoekingsbevel wordt geprint."
error_message = "Het maximum aantal aanvragen voor huiszoeking is overschreden, probeer over 10 minuten nog eens."

def controleer(wie, waar, wanneer):
    if pogingen <= MAX:
        verzend_button.enable()
    else:
        app.error(title="Maximum aantal aanvragen overschreden", text=error_message)
        time.sleep(600)  # 600 seconden (=10min) wachten
        verzend_button.enable()
    if wie==WIE and waar==WAAR and wanneer==WANNEER:
        print_bevel()
        app.info(title="Huiszoeking goedgekeurd", text=bevel)
        return
    else:
        error()
    return

def print_bevel():
    return

def error():
    app.info(title="Huiszoeking geweigerd", text=weiger_message)
    return

def verzend():
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
    name = TextBox(app, grid=[1,0], text="Voornaam Naam", width="fill")
    address_label = Text(app, text="Adres van de misdaad: ", grid=[0,1], font="Cambria")
    address = TextBox(app, grid=[1,1], text="Gebroeders Desmetstraat 1, 9000 Gent", width="fill")
    date_label = Text(app, text="Datum van de misdaad: ", grid=[0,2], font="Cambria")
    date = TextBox(app, grid=[1,2], text="dd/mm/jjjj", width="fill")
    verzend_button = PushButton(app, text="Verzend", command=verzend, grid=[1,3], width="fill")
    
    app.display()