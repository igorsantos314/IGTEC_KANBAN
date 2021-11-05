from tkinter import *
from tkinter import ttk
from time import sleep
import _thread as th

class beautiful_message:
    def __init__(self, window_mother) -> None:
        self.font_msg = 'Calibri 12 bold'

        self.dict_color_msg = {"info": "Green", "warning": "DarkOrange", "error": "Red", "wait": "Navy"}
        self.color_ask = 'SlateBlue'
        self.color_contrast = 'White'

        self.current_frame = window_mother
        self.frame_msg = None
        
    def msg(self, type, msg):
            
        #CASO JÁ EXISTA UMA MENSAGEM
        if self.frame_msg:
            #APAGA A ATUAL
            self.frame_msg.destroy()

        #FRAMA QUE ARMAZENA OS COMPONENTES DA MENSAGEM
        self.frame_msg = Frame(self.current_frame, width=self.getWith(), height=35, bg=self.dict_color_msg[type])
        self.frame_msg.pack(side=BOTTOM)

        #FOCAR APENAS NA MENSAGEM
        self.frame_msg.grab_set()

        #EXIBE A MENSAGEM
        lblMsg = Label(self.frame_msg, text=msg, font=self.font_msg, bg=self.dict_color_msg[type], fg=self.color_contrast)
        lblMsg.place(x=0, y=5)

        if type != 'wait':
            btOk = Button(self.frame_msg, text="OK", font=self.font_msg, fg=self.dict_color_msg[type], bg=self.color_contrast, bd=0, width=10, height=0, command=lambda: self.destroyMsg(None))
            btOk.place(x=self.getWith()-90, y=3)

            #FOCA NO BOTÃO
            btOk.focus_force()
        
            #PROCURA O APERTA DO ENTER
            btOk.bind("<Return>", self.destroyMsg)

    def ask(self, type, msg, command):
        
        print(type)
        
        #CASO JÁ EXISTA UMA MENSAGEM
        if self.frame_msg:
            #APAGA A ATUAL
            self.frame_msg.destroy()

        #FRAMA QUE ARMAZENA OS COMPONENTES DA MENSAGEM
        self.frame_msg = Frame(self.current_frame, width=self.getWith(), height=35, bg=self.color_ask)
        self.frame_msg.pack(side=BOTTOM)

        #FOCAR APENAS NA MENSAGEM
        self.frame_msg.grab_set()

        def yes(event):

            if type == 'wait':
                #SUCESSO
                th.start_new_thread(self.msg, ("wait", "AGUARDE ...", ))
                
                #EXECUTA A FUNÇÃO RECEBIDA DO BOTÃO
                th.start_new_thread(command, ())
            
            else:
                #EXECUTA O COMANDO EM SERIE
                command()

            try:
                #DESTROI O FRAME
                self.frame_msg.destroy()
            except:
                pass

        #EXIBE A MENSAGEM
        lblMsg = Label(self.frame_msg, text=msg, font=self.font_msg, bg=self.color_ask, fg=self.color_contrast)
        lblMsg.place(x=0, y=5)

        btYes = Button(self.frame_msg, text="Sim", font=self.font_msg, fg=self.color_ask, bg=self.color_contrast, bd=0, width=10, height=0, command=lambda: yes(None))
        btYes.place(x=self.getWith()-190, y=3)

        btNo = Button(self.frame_msg, text="Não", font=self.font_msg, fg=self.color_ask, bg=self.color_contrast, bd=0, width=10, height=0, command=lambda: self.destroyMsg(None))
        btNo.place(x=self.getWith()-90, y=3)

        #FOCA NO BOTÃO
        btYes.focus_force()
        
        #PROCURA O APERTA DO ENTER
        btYes.bind("<Return>", yes)

    def destroyMsg(self, event):
        #APAGA A MENSAGEM
        self.frame_msg.destroy()

    def getWith(self):
        #ATUALIZA O TK
        self.current_frame.update()

        #RETORNA O TAMANHO ATUAL DA TELA
        return self.current_frame.winfo_width()