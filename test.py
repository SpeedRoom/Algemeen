from guizero import *


app = App(title="Huiszoekingsbevel", height=480, width=640, layout='grid',
          bg="white")  # creates schermvakje van de grootte van het TFT shield

name_label = Text(app, text="Naam van de verdachte: ", grid=[0, 0, 1, 1], font="Cambria", )
name = TextBox(app, text="Voornaam Naam", grid=[1, 0, 2, 1], width=50)
address_label = Text(app, text="Adres van de misdaad: ", grid=[0, 1, 1, 1], font="Cambria")
address = TextBox(app, text="Gebroeders Desmetstraat 1, 9000 Gent", grid=[1, 1, 2, 1], width=50)
date_label = Text(app, text="Datum van de misdaad: ", grid=[0, 2, 1, 1], font="Cambria")
date = TextBox(app, text="dd/mm/jjjj", grid=[1, 2, 2, 1], enabled=False, width=50)
verzend_button = PushButton(app, text="Verzend", grid=[1, 3, 1, 1], width=20)
empty_label = Text(app, text="", grid=[0, 4, 1, 1])
empty_label2 = Text(app, text="", grid=[0, 5, 1, 1])
empty_label3 = Text(app, text="", grid=[0, 4, 1, 1])
empty_label4 = Text(app, text="", grid=[0, 5, 1, 1])
picture = Picture(app, image="Justitie.png",
                  grid=[0, 6, 3, 1])  # ook eens proberen zonder grid, eventueel nog met width

window = Window(app, title="Log in", height=480, width=640, layout='grid', bg="white")
name1_label = Text(window, text="Naam : ", grid=[0, 0, 1, 1], font="Cambria", )
name1 = TextBox(window, text="Voornaam Naam", grid=[1, 0, 2, 1], width=50)
name2_label = Text(window, text="Naam : ", grid=[0, 1, 1, 1], font="Cambria", )
name2 = TextBox(window, text="Voornaam Naam", grid=[1, 1, 2, 1], width=50)
name3_label = Text(window, text="Naam : ", grid=[0, 2, 1, 1], font="Cambria", )
name3 = TextBox(window, text="Voornaam Naam", grid=[1, 2, 2, 1], width=50)
login_button = PushButton(window, text="Log in", grid=[1, 3, 1, 1], width=20)
window.show(wait=True)


app.display()
