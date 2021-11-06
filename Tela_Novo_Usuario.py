from tkinter import *
from tkinter import font
from Persistencia import Persistencia
from Tela_Home import Tela_Home
from beautiful_message import beautiful_message
from util import util

class Tela_Novo_Usuario:

    def __init__(self) -> None:
        self.font_menu = 'Calibri 14 bold'
        self.font_titulo = 'Calibri 24 bold'
        self.font_msg = 'Calibri 12 bold'
        self.font_default = 'Calibri 14'
        self.font_usuario = 'Calibri 16 bold'
        self.font_default_labels = 'Calibri 14 bold'

        self.window()

    def window(self):
        
        self.windowNovoUsuario = Tk()
        self.windowNovoUsuario.title("IGTEC - Novo Usuário")
        self.windowNovoUsuario['bg'] = 'White'
        self.windowNovoUsuario.geometry(util().toCenterScreen(350, 400))

        #OBJETO DE MESAGENS
        self.msg = beautiful_message(self.windowNovoUsuario)

        #POSIÇÃO DO EIXO X COMUM
        posX = 70

        lblTitulo = Label(self.windowNovoUsuario, text='Novo Usuário', font=self.font_titulo, bg='White')
        lblTitulo.pack(pady=50)

        lblUsuario = Label(self.windowNovoUsuario, text='Usuário:', font=self.font_default, bg='White')
        lblUsuario.place(x=posX, y=120)
        
        etUsuario = Entry(self.windowNovoUsuario, font=self.font_menu)
        etUsuario.place(x=posX, y=150)

        lblSenha = Label(self.windowNovoUsuario, text='Senha:', font=self.font_default, bg='White')
        lblSenha.place(x=posX, y=190)

        etSenha = Entry(self.windowNovoUsuario, show='*', font=self.font_menu)
        etSenha.place(x=posX, y=220)

        lblRepetirSenha = Label(self.windowNovoUsuario, text='Repetir Senha:', font=self.font_default, bg='White')
        lblRepetirSenha.place(x=posX, y=260)

        etRepetirSenha = Entry(self.windowNovoUsuario, show='*', font=self.font_menu)
        etRepetirSenha.place(x=posX, y=290)

        btEntrar = Button(self.windowNovoUsuario, text='Salvar', font=self.font_menu, bd=0, fg='White', bg='DeepSkyBlue', width=20, command=lambda: salvar())
        btEntrar.place(x=posX, y=330)

        def salvar(event=None):
            
            usuario = etUsuario.get()
            senha = etSenha.get()
            repetirSenha = etRepetirSenha.get()

            if ' ' not in usuario:
                if len(senha) > 0 and len(usuario) > 0 :
                    #VERIFICA SE AS SENHAS SÃO IGUAIS
                    if senha == repetirSenha:
                        #VALIDA O LOGIN
                        if not Persistencia(usuario).existUsuario():
                            
                            #CADASTRA O USUÁRIO
                            Persistencia(usuario).createUsuario(
                                senha
                            )

                            #LIMPAR OS CAMPOS
                            limpar()

                            self.msg.msg("info", "Usuário Salvo !")

                        else:
                            self.msg.msg("error", "Nome de usuário já existe !")

                    else:
                        self.msg.msg("error", "As senhas são diferentes !")

                else:
                    self.msg.msg("error", "Usuário ou Senha vazio !")

            else:
                self.msg.msg("error", "Usuário não deve conter espeços !")

        def limpar():
            #LIMPAR OS CAMPOS
            etUsuario.delete(0, END)
            etSenha.delete(0, END)
            etRepetirSenha.delete(0, END)

        #FOCAR NO CAMPO DE USUÁRIO
        etUsuario.focus_force()
        
        #APERTA NA SENHA
        etRepetirSenha.bind("<Return>", salvar)

        self.windowNovoUsuario.mainloop()

#Tela_Novo_Usuario()