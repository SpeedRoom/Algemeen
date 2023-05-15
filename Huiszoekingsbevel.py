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
from TexSoup import TexSoup
from pdflatex import PDFLaTeX
import subprocess

soup = TexSoup(r'''\documentclass{article}
\usepackage{graphicx} % Required for inserting images
\usepackage[indent=0pt]{parskip}
\usepackage{caption}
\usepackage{subcaption}


\begin{document}
\begin{figure}
    \begin{subfigure}[b]{0.7\linewidth}
        \includegraphics[width=\textwidth]{Justitie.png}
    \end{subfigure}
    \begin{subfigure}[b]{0.2\linewidth}
        \includegraphics[width=\textwidth]{Politie.jpg}
    \end{subfigure}

\end{figure}
\par

\textbf{\Large{Betreft: Huiszoekingsbevel}}

De onderzoeksrechter bij de rechtbank van eerste aanleg te Gent,
Gelet op het strafdossier nr. 2023/2684;\par
Overwegende dat er ernstige aanwijzingen zijn dat Daan Peeters, geboren te Gent op 27 maart 1995, wonende te Gent, Stadhuissteeg 8, zich schuldig heeft gemaakt aan drugshandel;\par
Overwegende dat er redenen zijn om te vermoeden dat er in zijn woning bewijsmateriaal, geld of drugs aanwezig zijn die verband houden met de feiten;\par
Gelet op artikel 87bis van het Wetboek van Strafvordering;\par
\textbf{BEVEELT}\par
De officieren en agenten naam1, naam2, naam3 van gerechtelijke politie om zich te begeven naar de woning van Daan Peeters gelegen te Gent, Stadhuissteeg 8, en er een huiszoeking uit te voeren met het oog op het opsporen en in beslag nemen van alle voorwerpen die nuttig kunnen zijn voor de waarheidsvinding;\par
Dit bevel is geldig voor een periode van vijftien dagen te rekenen vanaf heden en kan slechts worden uitgevoerd tussen vijf uur 's morgens en negen uur 's avonds;\par
Gegeven te Gent op 16 mei 2023 om 9 uur.\par
De onderzoeksrechter,\par
\begin{figure}[h]
    \includegraphics[width=0.3\textwidth]{handtekening.png}
\end{figure}



\end{document}''')
naam1 = soup.find('naam1')
naam2 = soup.find('naam2')
naam3 = soup.find('naam3')


# MQTT stuff
broker = '192.168.1.61'  # IP-adres rpi
port = 1883  
topic_tetris = "esp_tetris/output"
topic_doolhof = "esp_doolhof/output"
topic_gsm = "esp_gsm/input"
client_id = "rp" 
username = 'sienp' 
password = 'sienp'  

WIE = "Daan Peeters"
WAAR = "Stadshal"
WANNEER = "datum"
MAX = 5

message_doolhof = ''
pogingen = 0

weiger_message = "Uw aanvraag voor een huiszoeking is geweigerd. Controleer of alle gegevens juist gespeld zijn. U heeft nog " + str(MAX - pogingen) + " pogingen over."
bevel = "Om aanvraag voor een huiszoeking is goedgekeurd. Uw huiszoekingsbevel wordt geprint."
error_message = "Het maximum aantal aanvragen voor huiszoeking is overschreden, probeer over 5 minuten nog eens."


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
        global message_doolhof
        print(f"Received `{msg.payload.decode('utf-8')}` from `{msg.topic}` topic")
        if msg.topic == "esp_doolhof/output":
                message_doolhof = str(msg.payload.decode('utf-8'))
                date.value = message_doolhof
            
    print(date.value)
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
    with open("out.tex", "w") as f:
        f.write(str(soup))
    subprocess.run(["pdflatex", "out.tex"])
    output_location = "/home/sienp/Documents"
    subprocess.run(["mv", "output.pdf", output_location])
    os.system("lp -d Canon_TS3300_series_USB_ output.pdf")  # printer name en file_name nog aanpassen, file bij in projectmap zetten
    publish(client, topic_gsm, "open")
    return


def error():
    app.info(title="Huiszoeking geweigerd", text=weiger_message)
    return


def verzend():
    global pogingen
    print("Aanvraag huiszoeking is verstuurd.")
    #verzend_button.disable()
    pogingen += 1
    wie = name.value
    waar = address.value
    wanneer = date.value
    controleer(wie, waar, wanneer)
    print(wie, waar, wanneer)
    return wie, waar, wanneer


def login():
    window.hide()
    soup.naam1.replace_with(name1.value)
    soup.naam2.replace_with(name2.value)
    soup.naam3.replace_with(name3.value)


app = App(title="Huiszoekingsbevel", height=480, width=640, layout='grid', bg="white")  # creates schermvakje van de grootte van het TFT shield
    
name_label = Text(app, text="Naam van de verdachte: ",grid=[0,0, 1, 1],  font="Cambria", )
name = TextBox(app, text="Voornaam Naam", grid=[1,0, 2, 1], width=50)
address_label = Text(app, text="Adres van de misdaad: ",grid=[0,1, 1, 1], font="Cambria")
address = TextBox(app, text="Gebroeders Desmetstraat 1, 9000 Gent", grid=[1,1, 2, 1], width=50)
date_label = Text(app, text="Datum van de misdaad: ", grid=[0,2, 1, 1], font="Cambria")
date = TextBox(app, text="dd/mm/jjjj", grid=[1,2, 2, 1], enabled=False, width=50)
verzend_button = PushButton(app, text="Verzend", command=verzend,grid=[1,3, 1, 1], width=20)
empty_label = Text(app, text="", grid=[0, 4, 1, 1])
empty_label2 = Text(app, text="", grid=[0, 5, 1, 1])
empty_label3 = Text(app, text="", grid=[0, 4, 1, 1])
empty_label4 = Text(app, text="", grid=[0, 5, 1, 1])
picture = Picture(app, image="Justitie.png", grid=[0,6, 3, 1])  # ook eens proberen zonder grid, eventueel nog met width

window = Window(app, title="Log in", height=480, width=640, layout='grid', bg="white")
name1_label = Text(window, text="Naam : ",grid=[0,0, 1, 1],  font="Cambria", )
name1 = TextBox(window, text="Voornaam Naam", grid=[1,0, 2, 1], width=50)
name2_label = Text(window, text="Naam : ",grid=[0,1, 1, 1],  font="Cambria", )
name2 = TextBox(window, text="Voornaam Naam", grid=[1,1, 2, 1], width=50)
name3_label = Text(window, text="Naam : ",grid=[0,2, 1, 1],  font="Cambria", )
name3 = TextBox(window, text="Voornaam Naam", grid=[1,2, 2, 1], width=50)
login_button = PushButton(window, text="Log in", command=login, grid=[1, 3, 1, 1], width=20)
window.show(wait=True)

client = connect_mqtt()
subscribe(client)
client.loop_start()

app.display()

client.loop_stop()  # stopt pas als gui geclosed wordt
