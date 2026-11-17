#bibliotecas importantes

import tkinter as tk
import pygame
import os
import sys
from tkinter import Canvas, ttk
from PIL import Image, ImageTk
from tkinter import Label, Button, Frame
import random

#alguma coisa importante que eu não entendi como funciona kkkk

script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

#definindo os paramentros da janela e suas caracteristicas e titulo

janela = tk.Tk()
janela.title('SIMULADOR DE ACELERADOR DE PATÍCULAS')
janela.geometry('700x600')
janela.configure(bg='black')

#adicionando o titulo principal na janela

titulo_simulador = tk.Label(janela,
    text='ACELERADOR/CANHÃO SIMPLES DE PARTÍCULAS',
    bg='green', 
    fg= 'white',
    font=('arial', 18, 'bold'),
    pady=10)
titulo_simulador.pack(fill='x', side='top')

#banco de imagens

img_canhao = Image.open('imagens/canhao.png')
img_canhao = img_canhao.resize((300, 200))
img_canhao = ImageTk.PhotoImage(img_canhao)

img_canhao2 = Image.open('imagens/canhao2.png')
img_canhao2 = img_canhao2.resize((300,200))
img_canhao2 = ImageTk.PhotoImage(img_canhao2)

img_botao = Image.open('imagens/botao.png')
img_botao = img_botao.resize((220, 150))
img_botao = ImageTk.PhotoImage(img_botao)

img_lampada_on = Image.open('imagens/lampada_on.png')
img_lampada_on = img_lampada_on.resize((100,100))
img_lampada_on = ImageTk.PhotoImage(img_lampada_on)

img_lampada_off = Image.open('imagens/lampada_off.png')
img_lampada_off = img_lampada_off.resize((100,100))
img_lampada_off = ImageTk.PhotoImage(img_lampada_off)

img_detector = Image.open('imagens/detector.png')
img_detector = img_detector.resize((150,150))
img_detector = ImageTk.PhotoImage(img_detector)

#label canhão

label_canhao = Label(janela, image= img_canhao, bd=0, highlightthickness= 0, bg='black')

label_canhao.place(x=-10, y=250)

label_canhao2 = Label(janela, image=img_canhao2, bd=0, highlightthickness=0, bg='black')

label_canhao2.place(x=1080,y=250)

#label trajetória da particula

particulas_canvas = Canvas(width=400, height=80, bg='black', bd=0, highlightthickness=0)
particulas_canvas.pack(pady = 10)

particulas_canvas2 = Canvas(width=400, height=80, bg='black', bd=0, highlightthickness=0)
particulas_canvas2.pack(pady = 10)

particulas_canvas.place(x=227, y=308)
particulas_canvas2.place(x=745, y=308)

label_trajetoria = Label(janela, bd=0, highlightthickness=0, bg='black')

label_trajetoria.place(x=-10, y=250)

#canva detector e quadro com resultado

canva_detector = Canvas(width=150, height=150, bg= 'black', bd=0, highlightthickness=0)
canva_detector.create_image(75,75, image= img_detector)
canva_detector.pack(pady=10)

canva_detector.place(x=627, y=258)


canva_quadro_resultado = Canvas(width=600, height=237, bg='#112F2C', bd=0, highlightthickness=4, highlightbackground='white')
canva_quadro_resultado.place(x=400, y=400)
canva_quadro_resultado.create_text(140,18,text='QUADRO DE APURAÇÃO DE RESULTADO:', fill='white', font=("Arial", 10, "bold"))

#lista de particulas

lista_particulas ={
     'red': 'Elétron',
     'blue': 'Nêutron',
     'green': 'Próton',
     'orange': 'Fóton'
}

#lampadas canvas

canva_lampada = Canvas(width=100, height=100, bd=0, highlightthickness=0, bg='black')

canva_lampada.place(x=650, y=158)

#detector ligando

img_lampada_id1 = canva_lampada.create_image(50,50, image=img_lampada_off)

def detectando():
     canva_lampada.itemconfig(img_lampada_id1, image= img_lampada_on)

def desligando_detector():
     canva_lampada.itemconfig(img_lampada_id1, image= img_lampada_off)

#sons

pygame.mixer.init()

som_botao = pygame.mixer.Sound('sons/botao.mp3')
som_disparo = pygame.mixer.Sound('sons/disparo.mp3')
som_disparo.set_volume(0.2)
som_detector = pygame.mixer.Sound('sons/detector_som.mp3')

def tocar_som_botao():
     som_botao.play()

def tocar_som_disparo():
     som_disparo.play()

def tocar_som_detector():
     som_detector.play()

#adcionando as particulas primeiro canhao

def disparar_particula ():

     cores = ['red', 'blue', 'green', 'orange'] 
     cor = random.choice(cores)

     particula = particulas_canvas.create_oval(25,50,50,25, width=3, fill= cor)
     particula2 = particulas_canvas2.create_oval(375, 35, 395, 55, width=3, fill= cor)

     mover_particula(particula,particula2, cor)

    
def mover_particula(p1, p2, cor):
    
    particulas_canvas.move(p1, 5, 0)
    particulas_canvas2.move(p2, -5, 0)

    x1, y1, x2, y2 = particulas_canvas.coords(p1)
    a1, b1, a2, b2 = particulas_canvas2.coords(p2)
    if x2 < 400 and a1>0:
         particulas_canvas.after(16, lambda: mover_particula(p1,p2,cor))                 
    else:
         detectando()
         tocar_som_detector()
         nome_particula = lista_particulas.get(cor,'Desconhecida')
         canva_quadro_resultado.delete("detect")
         canva_quadro_resultado.create_text(160, 58, text=f'PARTICULA DETECTADA: {nome_particula}', fill='yellow',font=("Arial", 12, "bold"), tag='detect')    
         particulas_canvas.after(500, desligando_detector)
         particulas_canvas.delete(p1)
         particulas_canvas2.delete(p2)

#adcionando as particulas primeiro canhao


    
#botão configuração e canva

canva_botao_atirar = tk.Canvas(janela, width=220, height=150, bd=0, highlightthickness=4, bg='#112F2C')
canva_botao_atirar.create_image(115,78, image= img_botao)
canva_botao_atirar.place(x=10, y=490)

#botão configuração

def disparar_botao():
     tocar_som_disparo()
     disparar_particula()
     tocar_som_botao()
     
     
canva_botao_atirar.bind("<Button-1>", lambda e:disparar_botao())

janela.mainloop()
