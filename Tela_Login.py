from tkinter import *
from tkinter import font
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

        #POSIÇÃO DO EIXO X COMUM
        posX = 70

        lblTitulo = Label(self.windowLogin, text='Login', font=self.font_titulo, bg='White')
        lblTitulo.pack(pady=50)

        lblUsuario = Label(self.windowLogin, text='Usuário:', font=self.font_default, bg='White')
        lblUsuario.place(x=posX, y=120)
        
        etUsuario = Entry(self.windowLogin, font=self.font_default)
        etUsuario.place(x=posX, y=150)

        lblSenha = Label(self.windowLogin, text='Senha:', font=self.font_default, bg='White')
        lblSenha.place(x=posX, y=190)

        etSenha = Entry(self.windowLogin, font=self.font_default)
        etSenha.place(x=posX, y=220)

        self.windowLogin.mainloop()

Tela_Login()