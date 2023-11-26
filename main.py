from cProfile import label
from tkinter import *
from tkinter.ttk import Labelframe
from turtle import right
from click import command
import tkintermapview
import requests
import threading


root = Tk()
root.title('BOOTES')
root.iconbitmap("icon/bootes.ico")
# root.geometry("1450x800")
root.configure(bg='#313131')

def get_info():
    try:
        resposta = requests.get('http://192.168.1.100/dados')
        resposta.raise_for_status() 
        dados = resposta.text
        dados_separados = dados.split("e")
        
        if len(dados_separados) >= 4:
            hum = str(dados_separados[1][0:4] + '%')
            tmp = str(dados_separados[0][0:4] + ' °C')
            pres = str(dados_separados[2] + ' atm')
            altd = str(dados_separados[3]+ ' m')
            humidade1.configure(text=hum)
            temperatura1.configure(text=tmp)
            press1.configure(text=pres)
            alt1.configure(text=altd)
            print(hum, tmp, pres, altd)
        else:
            print("Dados incompletos ou fora do formato esperado.")
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
    
    root.after(5000, get_info)

threading.Thread(target=get_info).start()

def get_info2():
    try:
        resposta2 = requests.get('http://192.168.1.100/gps')
        resposta2.raise_for_status() 
        dados2 = resposta2.text
        dados_separados2 = dados2.split("e")
        lat = float(dados_separados2[1])
        lng = float(dados_separados2[0])
        map_widget2.set_position(lng, lat, text='cansat', marker=True)
        print(lat, lng)
    except (requests.RequestException, ValueError) as e:
        print(f"Erro na requisição ou conversão de dados: {e}")
    
    root.after(20000, get_info2)

threading.Thread(target=get_info2).start()

#User Interface

my_label = LabelFrame(root, width=1184, height=92, borderwidth=0, bg='#313131')
my_label.pack(side=TOP, pady=30, padx=30)

my_labe2 = LabelFrame(root, width=592, height=592, borderwidth=0, bg='#313131')
my_labe2.pack(side=LEFT, pady=20, padx=30)

my_label3 = LabelFrame(root, width=892, height=592, borderwidth=0, bg='#232323')
my_label3.pack(side=RIGHT, padx=20, pady=30)

# container: TOP
img = PhotoImage(file='icon/bootesicon3.png')
logo = Label(my_label, image=img, bg='#313131')
logo.grid(column=0, row=0)
head = Label(my_label,
    text='Estação de Monitoramento',
    bg= '#313131',
    fg='#27A436',
    font=('Nunito', 35, 'bold')
)
head.grid(column=1, row=0)

map_widget2 = tkintermapview.TkinterMapView(my_labe2, width=592, height=592, corner_radius=18)
map_widget2.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
map_widget2.set_zoom(20)
map_widget2.pack()  

temperatura1 = Label(my_label3, text='', bg='#232323', fg='#FFFFFF', font=('Nunito', 60, 'bold'))
temperatura1.grid(column=0, row=0, padx=80, pady=37)
temperatura = Label(my_label3, text='Temperatura', bg= '#232323', fg='#27A436', font=('Nunito', 20, 'bold'))
temperatura.grid(column=0, row=1, padx=100, pady=33)

humidade1 = Label(my_label3, text='', bg='#232323', fg='#FFFFFF', font=('Nunito', 60, 'bold'))
humidade1.grid(column=1, row=0, padx=80, pady=37)
humidade = Label(my_label3, text='Umidade', bg= '#232323', fg='#27A436', font=('Nunito', 20, 'bold'))
humidade.grid(column=1, row=1, padx=100, pady=33)

press1 = Label(my_label3, text='', bg='#232323', fg='#FFFFFF', font=('Nunito', 60, 'bold'))
press1.grid(column=0, row=2, padx=80, pady=37)
press = Label(my_label3, text='Pressão atmosférica', bg= '#232323', fg='#27A436', font=('Nunito', 20, 'bold'))
press.grid(column=0, row=3, padx=100, pady=33 )

alt1 = Label(my_label3, text='00.0m', bg='#232323', fg='#FFFFFF', font=('Nunito', 60, 'bold'))
alt1.grid(column=1, row=2, padx=80, pady=37)
alt = Label(my_label3, text='Altitude', bg= '#232323', fg='#27A436', font=('Nunito', 20, 'bold'))
alt.grid(column=1, row=3, padx=100, pady=33)


root.mainloop()
