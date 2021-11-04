from tkinter import *
from tkinter import font
from typing import List
from tkinter import ttk
from rsa import common
from Persistencia import Persistencia
from util import util
import _thread as th
from beautiful_message import beautiful_message

class Tela_Novo_Quadro:
    
    def __init__(self, usuario) -> None:
        self.usuario = usuario

        self.font_menu = 'Calibri 14 bold'
        self.font_titulo = 'Calibri 24 bold'
        self.font_msg = 'Calibri 12 bold'
        self.font_default = 'Calibri 14'
        self.font_usuario = 'Calibri 16 bold'
        self.font_default_labels = 'Calibri 14 bold'

        self.color_theme = 'Black'
        self.color_contrast = 'White'
        self.dict_color_msg = {"info": "Green", "warning": "DarkOrange", "error": "Red", "wait": "Navy"}
        self.color_ask = 'SlateBlue'
        
        self.height_window = 532

        #CARREGA AS IMAGENS PARA O SISTEMA
        #self.setImagensBase64()

        self.current_frame = None
        self.frame_msg = None

        self.current_setor = None
        self.new_setor = None

        self.window()
    
    def window(self):
        self.windowNovoQuadro = Tk()
        self.windowNovoQuadro.geometry(util().toCenterScreen(450, 300))
        self.windowNovoQuadro['bg'] = 'White'
        self.windowNovoQuadro.title("IGTEC - NOVO QUADRO")
        self.windowNovoQuadro.resizable(False, False)

        self.lblTitulo = Label(self.windowNovoQuadro, text='Novo Quadro', font=self.font_titulo, bg=self.color_contrast)
        self.lblTitulo.pack(pady=10)
        
        posX = 10

        lblNome = Label(self.windowNovoQuadro, text='Nome do Quadro:', font=self.font_default, bg='White')
        lblNome.place(x=10, y=80)

        etNome = Entry(self.windowNovoQuadro, font=self.font_menu)
        etNome.place(x=posX, y=110)

        lblSubtitulo = Label(self.windowNovoQuadro, text='Descrição:', font=self.font_default, bg='White')
        lblSubtitulo.place(x=230, y=80)

        etSubtitulo = Entry(self.windowNovoQuadro, font=self.font_menu)
        etSubtitulo.place(x=230, y=110)

        #COR
        lblCor = Label(self.windowNovoQuadro, text='Cor:', font=self.font_default, bg='White')
        lblCor.place(x=posX, y=150)

        comboCor = ttk.Combobox(self.windowNovoQuadro, font=self.font_default_labels, width=18, state="readonly")

        comboCor['values'] = tuple(
            ['SpringGreen', 'Tomato', 'Aquamarine', 'Gray', 'Cyan'])
        comboCor.current(0)
        comboCor.place(x=posX, y=180)

        def criar():
            if len(etNome.get().replace(" ", "")) > 0 and len(etSubtitulo.get().replace(" ", "")) > 0:
                
                #CRIAR QUADRO
                Persistencia(self.usuario).createBoard(
                    etNome.get(),
                    etSubtitulo.get(),
                    comboCor.get()
                )
                
                #LIMPAR CAMPOS
                limpar()

        def limpar():
            #LIMPAR CAMPOS
            etNome.delete(0, END)
            etSubtitulo.delete(0, END)
            comboCor.current(0)

        def sair():
            self.windowNovoQuadro.destroy()

        btSalvar = Button(self.windowNovoQuadro, text='Criar', font=self.font_default_labels, fg='White', bg='Black', bd=0, width=9, command= criar)
        btSalvar.place(x=10, y=240)

        btCancelar = Button(self.windowNovoQuadro, text='Cancelar', font=self.font_default_labels, fg='White', bg='Black', bd=0, width=9, command= sair)
        btCancelar.place(x=120, y=240)
        
        #FOCAR NO CAMPO DE NOME
        etNome.focus_force()

        self.windowNovoQuadro.mainloop()

#Tela_Novo_Quadro('igorsantos314')