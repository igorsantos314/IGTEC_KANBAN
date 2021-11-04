from tkinter import *
from tkinter import font
from Persistencia import Persistencia
from Tela_Home import Tela_Home
from beautiful_message import beautiful_message
from util import util

class Tela_Login:

    def __init__(self) -> None:
        self.font_menu = 'Calibri 14 bold'
        self.font_titulo = 'Calibri 24 bold'
        self.font_msg = 'Calibri 12 bold'
        self.font_default = 'Calibri 14'
        self.font_usuario = 'Calibri 16 bold'
        self.font_default_labels = 'Calibri 14 bold'

        self.window()

    def window(self):
        
        self.windowLogin = Tk()
        self.windowLogin.title("IGTEC - Login")
        self.windowLogin['bg'] = 'White'
        self.windowLogin.geometry(util().toCenterScreen(350, 400))

        #OBJETO DE MESAGENS
        self.msg = beautiful_message(self.windowLogin)

        #POSIÇÃO DO EIXO X COMUM
        posX = 70

        lblTitulo = Label(self.windowLogin, text='Login', font=self.font_titulo, bg='White')
        lblTitulo.pack(pady=50)

        lblUsuario = Label(self.windowLogin, text='Usuário:', font=self.font_default, bg='White')
        lblUsuario.place(x=posX, y=120)
        
        etUsuario = Entry(self.windowLogin, font=self.font_menu)
        etUsuario.place(x=posX, y=150)

        lblSenha = Label(self.windowLogin, text='Senha:', font=self.font_default, bg='White')
        lblSenha.place(x=posX, y=190)

        etSenha = Entry(self.windowLogin, show='*', font=self.font_menu)
        etSenha.place(x=posX, y=220)

        btEntrar = Button(self.windowLogin, text='Entrar', font=self.font_menu, bd=0, fg='White', bg='DodgerBlue', width=20, command=lambda: login())
        btEntrar.place(x=posX, y=290)

        btNovoUsuario = Button(self.windowLogin, text='Novo Usuário', font=self.font_menu, bd=0, fg='White', bg='DeepSkyBlue', width=20)
        btNovoUsuario.place(x=posX, y=330)

        def login():
            
            usuario = etUsuario.get()
            senha = etSenha.get()

            #VALIDA O LOGIN
            if Persistencia(usuario).login(senha):
                
                #FECHAR LOGIN
                self.windowLogin.destroy()

                #ABRE A TELA DE QUADROS ENVIANDO O USUÁRIO
                Tela_Home(usuario)
            
            else:
                self.msg.msg("error", "Senha ou Usuário Incorretos !")
        
        #FOCAR NO CAMPO DE USUÁRIO
        etUsuario.focus_force()
        
        self.windowLogin.mainloop()

Tela_Login()