from tkinter import *
from tkinter import ttk
import base64
from time import sleep
from tkinter import font
from typing import List
from Persistencia import Persistencia
from beautiful_message import beautiful_message
from util import util
import _thread as th

class Nova_Tarefa:

    def __init__(self, usuario, board_titulo) -> None:
        
        #TITULO DO QUADRO E USUÁRIOS
        self.board_titulo = board_titulo
        self.usuario = usuario
        
        self.font_menu = 'Calibri 14 bold'
        self.font_titulo = 'Calibri 24 bold'
        self.font_msg = 'Calibri 12 bold'
        self.font_default = 'Calibri 14'
        self.font_usuario = 'Calibri 16 bold'
        self.font_default_labels = 'Calibri 14 bold'

        self.window()

    def window(self):
        self.windowNovaTarefa = Tk()
        self.windowNovaTarefa.geometry(util().toCenterScreen(430, 270))
        #self.windowQuadro.overrideredirect(True)
        self.windowNovaTarefa['bg'] = 'White'
        self.windowNovaTarefa.title("IGTEC - NOVA TAREFA")
        self.windowNovaTarefa.resizable(False, False)

        #OBEJTOS PARA MENSAGENS
        self.msg = beautiful_message(self.windowNovaTarefa)

        #TITULO
        lblTitulo = Label(self.windowNovaTarefa, text='NOVA TAREFA', font=self.font_titulo, bg='White')
        lblTitulo.pack(pady=10)

        #ATIVIDADE
        lblAtividade = Label(self.windowNovaTarefa, text='Atividade:', font=self.font_default_labels, bg='White')
        lblAtividade.place(x=10, y=80)

        etAtividade = Entry(self.windowNovaTarefa, font=self.font_default_labels, width=40)
        etAtividade.place(x=10, y=110)

        #DATA
        lblData = Label(self.windowNovaTarefa, text='Data:', font=self.font_default_labels, bg='White')
        lblData.place(x=10, y=150)

        etData = Entry(self.windowNovaTarefa, font=self.font_default_labels, width=10)
        etData.insert(0, util().getData())
        etData.place(x=10, y=180)

        #PRIORIDADE
        lblPrioridade = Label(self.windowNovaTarefa, text='Prioridade:', font=self.font_default_labels, bg='White')
        lblPrioridade.place(x=140, y=150)

        comboPrioridade = ttk.Combobox(self.windowNovaTarefa, font=self.font_default_labels, width=10, state="readonly")

        comboPrioridade['values'] = tuple(
            ['I', 'II', 'III', 'IV', 'V'])
        comboPrioridade.current(0)
        comboPrioridade.place(x=140, y=180)
        
        #COR
        lblCor = Label(self.windowNovaTarefa, text='Cor:', font=self.font_default_labels, bg='White')
        lblCor.place(x=290, y=150)

        comboCor = ttk.Combobox(self.windowNovaTarefa, font=self.font_default_labels, width=10, state="readonly")

        comboCor['values'] = tuple(
            ['SpringGreen', 'Tomato', 'Aquamarine', 'Gray', 'Cyan'])
        comboCor.current(0)
        comboCor.place(x=290, y=180)

        def adicionar():
            
            if len(etAtividade.get().replace(" ", "")) > 0:
                
                #SALVAR TAREFA NA COLUNA TO DO DO QUADRO ESPECIFICO
                Persistencia(self.usuario).adicionarTarefas(
                    self.board_titulo,
                    etAtividade.get(),
                    comboCor.get(),
                    etData.get(),
                    comboPrioridade.get()
                )

                th.start_new_thread(beautiful_message(self.windowNovaTarefa).msg, ("info", "SALVO !", ))

                #LIMPAR OS CAMPOS
                limpar()

        def limpar():
            etAtividade.delete(0, END)
            etData.delete(0, END)

            comboPrioridade.current(0)
            comboCor.current(0)

            etData.insert(0, util().getData())
            
        btSalvar = Button(self.windowNovaTarefa, text='Salvar', font=self.font_default_labels, fg='White', bg='Black', bd=0, width=10, command= lambda: self.msg.ask(None, "Salvar Tarefa?", adicionar))
        btSalvar.place(x=10, y=220)

        #FOCAR NO CAMPO DE ATIVIDADE
        etAtividade.focus_force()

        self.windowNovaTarefa.mainloop()

Nova_Tarefa('igorsantos314', 'Proj2')