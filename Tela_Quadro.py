from tkinter import *
from tkinter import ttk
import base64
from time import sleep
from tkinter import font
from typing import List
from Persistencia import Persistencia
from Tela_Nova_Tarefa import Nova_Tarefa
from util import util
import _thread as th

class Tela_Quadro:
    
    def __init__(self, usuario, board) -> None:
        
        self.board = board
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
        self.setImagensBase64()

        self.current_frame = None
        self.frame_msg = None

        self.current_setor = None
        self.new_setor = None

        self.window()
    
    def window(self):
        self.windowQuadro = Tk()
        self.windowQuadro.geometry(util().toCenterScreen(925, 600))
        #self.windowQuadro.overrideredirect(True)
        self.windowQuadro['bg'] = 'White'
        self.windowQuadro.title("IGTEC - BOARD")
        self.windowQuadro.resizable(False, False)

        # --- INFORMAÇÕES DO QUADRO ---
        self.frameMiniQuadro = Frame(self.windowQuadro, bg=self.color_theme, width=925, height=90)
        self.frameMiniQuadro.place(x=0, y=0)
        
        #FRAME DA BARRA LATERAL COLORIDA
        frameFaixa = Frame(self.frameMiniQuadro, bg=self.board["Color"], width=10, height=90)
        frameFaixa.place(x=0, y=0)
        
        self.lblTitulo = Label(self.frameMiniQuadro, text=self.board["Titulo"], font=self.font_titulo, fg=self.color_contrast, bg=self.color_theme)
        self.lblTitulo.place(x=10, y=10)
    
        self.lblSubtitulo = Label(self.frameMiniQuadro, text=self.board["Subtitulo"], font=self.font_default, fg=self.board["Color"], bg=self.color_theme)
        self.lblSubtitulo.place(x=10, y=50)

        # -- MENU --
        def popup(event):
            #ABRE O MENU ONDE O MOUSE ESTIVER
            self.menuPopup.post(event.x_root, event.y_root)
        
        #MENU POPUP
        self.menuPopup = Menu(self.windowQuadro, font=self.font_default, fg='Black', bg='White', bd=0, tearoff=0)
        self.menuPopup.add_command(label="Novo Atividade", command=lambda: self.novaTarefa())
        self.menuPopup.add_separator()
        self.menuPopup.add_command(label="Voltar", command=lambda: self.voltar())
        
        #MENU DE 3 PONTOS
        imagem_menu = PhotoImage(data=base64.b64decode(self.imagem_menu))
        btMenu = Button(self.windowQuadro, image=imagem_menu, bd=0, height=60, width=30, bg=self.color_theme)
        btMenu.image = imagem_menu
        btMenu.place(x=885, y=10)

        btMenu.bind("<Button-1>", popup)

        # -- COLUNAS --
        width_colunas = 13

        self.frameDivisoes = Frame(self.windowQuadro, bg='White')
        self.frameDivisoes.place(x=0, y=100)

        lblToDo = Label(self.frameDivisoes, text='To Do', font=self.font_titulo, bg='White', width=width_colunas)
        lblToDo.pack(side=LEFT)
        
        lblDoing = Label(self.frameDivisoes, text='Doing', font=self.font_titulo, bg='White', width=width_colunas)
        lblDoing.pack(side=LEFT)

        lblOnHold = Label(self.frameDivisoes, text='On Hold', font=self.font_titulo, bg='White', width=width_colunas)
        lblOnHold.pack(side=LEFT)

        lblDone = Label(self.frameDivisoes, text='Done', font=self.font_titulo, bg='White', width=width_colunas)
        lblDone.pack(side=LEFT)

        #CRIAR COLUNAS E EXIBIR TAREFAS
        self.createColunas()
        self.exibirPostIts()
        
        #FOCAR NA TELA
        self.windowQuadro.focus_force()

        self.windowQuadro.bind("<F5>", self.atualizarTarefas)
        self.windowQuadro.mainloop()

    # -- COLUNAS --
    def atualizarTarefas(self, event):
        #PEGA OS DADOS DO QUADRO ATUALIZADOS
        self.board = Persistencia(self.usuario).getBoard(self.board['Titulo'])
        
        #APAGA TUDO
        self.destroyColunas()

        #RECONSTROI
        self.createColunas()
        self.exibirPostIts()

    def createColunas(self):
        # -- LINHAS DA DIVISÕES --
        self.createFrameToDo()
        self.createFrameDoing()
        self.createFrameOnHold()
        self.createFrameDone()

    def destroyColunas(self):
        self.frameToDo.destroy()
        self.frameDoing.destroy()
        self.frameOnHold.destroy()
        self.frameDone.destroy()

    # -- CRIAÇÃO DE FRAMES --
    def createFrameToDo(self):

        width_frame = 210
        height_frame = 450

        main_frame = Frame(self.windowQuadro, bg='White', width=width_frame, height=height_frame)
        main_frame.place(x=0, y=144)

        my_canvas = Canvas(main_frame, bg='White', bd=0, width=width_frame, height=height_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # -- FRAME TO DO --
        self.frameToDo = Frame(my_canvas, bg='White', width=width_frame, height=height_frame)
        self.frameToDo.place(x=0, y=144)

        my_canvas.create_window((0,0), window=self.frameToDo, anchor="nw")

    def createFrameDoing(self):

        width_frame = 210
        height_frame = 450

        main_frame = Frame(self.windowQuadro, bg='White', width=width_frame, height=height_frame)
        main_frame.place(x=230, y=144)

        my_canvas = Canvas(main_frame, bg='White', bd=0, width=width_frame, height=height_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # -- FRAME TO DO --
        self.frameDoing = Frame(my_canvas, bg='White', width=width_frame, height=height_frame)
        self.frameDoing.place(x=0, y=144)

        my_canvas.create_window((0,0), window=self.frameDoing, anchor="nw")

    def createFrameOnHold(self):

        width_frame = 210
        height_frame = 450

        main_frame = Frame(self.windowQuadro, bg='White', width=width_frame, height=height_frame)
        main_frame.place(x=460, y=144)

        my_canvas = Canvas(main_frame, bg='White', bd=0, width=width_frame, height=height_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # -- FRAME TO DO --
        self.frameOnHold = Frame(my_canvas, bg='White', width=width_frame, height=height_frame)
        self.frameOnHold.place(x=0, y=144)

        my_canvas.create_window((0,0), window=self.frameOnHold, anchor="nw")

    def createFrameDone(self):

        width_frame = 210
        height_frame = 450

        main_frame = Frame(self.windowQuadro, bg='White', width=width_frame, height=height_frame)
        main_frame.place(x=690, y=144)

        my_canvas = Canvas(main_frame, bg='White', bd=0, width=width_frame, height=height_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        # -- FRAME TO DO --
        self.frameDone = Frame(my_canvas, bg='White', width=width_frame, height=height_frame)
        self.frameDone.place(x=0, y=144)

        my_canvas.create_window((0,0), window=self.frameDone, anchor="nw")

    # -- EXIBIR POST ITS --
    def exibirPostIts(self):
        #POSIÇÃO INICIAL
        posx = 40

        for postIt in self.board['To do'][::-1]:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameToDo, postIt)

        for postIt in self.board['Doing']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameDoing, postIt)

        for postIt in self.board['On Hold']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameOnHold, postIt)

        for postIt in self.board['Done']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameDone, postIt)

    def setPostIt(self, frame, postIt):
        #print(postIt)

        # -- MENU --
        def popup(event):
            menuPopup.post(event.x_root, event.y_root)

        framePostIt = Frame(frame, bg=postIt['Color'], width=200, height=90)
        framePostIt.pack(side=TOP, pady=10, padx=5)

        #MENU POPUP
        menuPopup = Menu(framePostIt, font=self.font_msg, fg='Black', bg=postIt['Color'], bd=0, tearoff=0)
        menuPopup.add_command(label="Editar", command=lambda: print(postIt))
        menuPopup.add_command(label="Excluir", command=lambda: 'imprimir(None)')
        menuPopup.add_separator()
        menuPopup.add_command(label="Sair", command=lambda: 'editar(None)')

        lblAtividade = Label(framePostIt, text=postIt['Atividade'], font=self.font_menu, bg=postIt['Color'])
        lblAtividade.place(x=0, y=0)
        
        lblData = Label(framePostIt, text=postIt['Data'], font=self.font_default, bg=postIt['Color'])
        lblData.place(x=0, y=30)
        
        lblPrioridade = Label(framePostIt, text=postIt['Prioridade'], font=self.font_menu, bg=postIt['Color'])
        lblPrioridade.place(x=0, y=60)

        framePostIt.bind("<Button-3>", popup)
        
    def formatSubtitulo(self, subtitilo):
        #FORMATA A STRING PARA NÃO UTRAPASSAR A QUANTIDADE DE CARACTERES
        if len(subtitilo) > 16:
            return f"{subtitilo[:16]}..."
        return subtitilo

    def voltar(self):
        self.windowQuadro.destroy()

    def novaTarefa(self):
        Nova_Tarefa(self.usuario, self.board['Titulo'])

    def setImagensBase64(self):
        self.imagem_usuario = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAAEf0lEQVR4nO3bX4hWRRjH8Y9rllC6mpoFuW1/F7GorjK7qNAu666LMrEiSiiSoIiCKItAoj8oJEEXlRFkRUFQUd3URV0UkaTZZn+3wIz1X7p2YeV2MWdxW99z3vfMnHPW8P3Cc/Ge9535Pc+cM2dmnpmXLl26dDmOmdKg1nxciAGchVk4JftuBPswhG+xFb836Fst9OAabMA3GC1p2/AslmZ1/W+Yh0fxq/JB59kvWIO5DcZRmtl4Wnicqwp8oo3gSaH7HDNMwUqhz9YV+ETbiRVNBNeOmdikucAn2lvCkzcpLMKPbRxswn7AwppjPYol2J3g9N/4Cu9ktiW7FlvfLiyuNeJxLMHBSEd/w93CSDGR07Ba6N8xdY9ooBEWib/zbzgy8SliBt6M1Nilxu4wS3yff0G5WecUvBSp9T16o6MscCj2rnyBEyM0T8KXkZqvRegVsjLSkVFcnaC7LEF3eYLuf5gtfpLzdQX6g5HaO3UwY+xkkfGQ8IaO4b3IcuN5N7LcfDyYKj4HB8Q/hqtSHcCdCfoj2iyg2j0Bq3U2dOUxklB2jD8Syp6Mu4p+UNQAPbg5QZz4rjOeMxLL36IgzqIGWIoFieKXJJaHixPL9+HKmIIbxPe9MdstjOexTMfeCvxYHyMeO/xMtHtixDPuq8iHLWWFT69IeBR7cH5ZB4Tk6b6KfDis5PtoaUXCYzao3PukT8gOV+lDyxlp3ktwoISznTCAz3BtB7+9Dp/jghp8OIoTcn7cX7E4oVu9jU/wCj4Wsr2EO34VbsLlNWjD2a0u5jXAzJqcgCsya5oZrS7mdYGU2d+xSqkGOG7Ia4Aq5vDHGgdaXcxrgP01OjJZtIwprwGGanRksvi51cW8Bhis0ZHJomVMecPgVmH2VOX5gd3YLGSWf8o+j/XLGULioh/n4FKcWqH2qIj03DZpU8+d2IgbxU2s+oXE5kbxmyXRiyHC4YSyQgczh5epdojtyep8GX9G+LUuRrRMSvpgJpKavemEeVir3PZcVEKkR5irt6v8U5wbG00CffioA/+GJDyNa9pU/lRK5RUwFc+08Gu8PZwiMFf+kZcXNXvKLI+ifcT92owm7e7eLjyX892CDso3QQ/OzPlug5CRSmKW/GHosdTKK+BxrX3bocJl/YockcO4vSqRCFZlPrTy7YaqxV7PEfoHt1Yt1gG3yQ/+1ToEe4UDSXlPwlrhrVw3U/FEjh+j2K7GjNZC4cWYJ/6+cA64LvrxYYH+sOoTukexWPFp0BHcK+zqVMV0YZOkSPcALqtQs5DFip+EUeFE2P3SVnVz8ID2i6FhDQY/xkLhQFK7qeghoWvcIWx0Tiuoc5qwoboKH+CvDurfLuGxT53J9eJ5XF+izCF8J2x77c2uzc7sPOUOVG0ShuFJT+EtFx75dnerKtuhhnE+lV5heEo5UtPO9gvDbZ0bN8nMwSPCMrSqwIeEVV2VabLa6RF2ZNc7kmPs1A5nZdYJyYzaFl1NLmfn4SJh17dPuJvj/zS1R0jAjP1parhB37p06dLl+ORfOBG/whDjMksAAAAASUVORK5CYII='
        
        self.imagem_menu = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAABkUlEQVR4nO3awS5DQRTG8W+wrETtxLpWZUsEb8QzEI/gpTSSEu2KrdhhwVL7t2g0chW3qTkj+v22Pcl89yQ393RmJDMzM7MAwAFwBbzy2StwCeyXzpkFsAo8TXjwqkegGZVrIWohSduSVmrUNSXtZM4yFtmARqbamUQ24E9yA0oHKM0NCFzrforau2wpSgGWgE6NOeAcWIrKlaIWkiSgIelQ0pakxcrPA0nXks5SSi+RuczMzOZU6BwgScCGpLYmzwH9lNJNdKYwwCkw/GYKHAInpXNmAWz88PAfm9CKyhX5Z6iteq9ckrSZOctYZAOq7/xv1c7E+wGlA5TmBgSuNchUO5PIBvQlUaMOSb3MWcoATmoMQseRmUqMwi2NvvOTRuFeSuk2OpOZmdmcij4aW5Z0pK+3xHoaHY09R+YKwehw9KLGjlCHwMPRMMBejYd/txuVK/LP0NoUtevZUlR4P6B0gNLcgNIBSotswDTXXv7fFRlGl6Ufa3wCHwi8LB0K2Ae6fH1dvgvslc5pZmZm8+EN6vTRQDQnGnkAAAAASUVORK5CYII='
        self.imagem_kanban = 'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAABmJLR0QA/wD/AP+gvaeTAAAB8ElEQVR4nO3cS07DMBSF4cNjCyyEWTpjdyyIQTtjwmJYBTCoLEWiVZrUN8fX/j/JwxTnHLt5IJAAAAAAAAAwiif3BDY6SHqR9O2eyGgmSR+SfiV9mucylHnw8/HmnNQIrgVfBrsgyFLw7IIga4JnF1S0JXh2QQUHSSdtD76M970nnt29K76ML7H6VyF4E4I3IXiTSdJR9wd/0vlCXdtB0mvA59q1vuK7fZeUKfj5SP+1ljX4MtLuguzBp94FNS6uR51Dqm3Lk3W6XZB9xaffBdlX/KWR6l1SDys+en6hnCt+Up0VH/WAF3HO/yydXFTwLT9Zz+cXbukka2r9q6bM70cx53/RHgVkDL6LAjIHn7qAHoJPWUBPwacqoMfg0xTQ8rukGre74e6dQG8rfogCMgTfZQGZgu+qgIzBd1NAqxfXYQqoaY8VTwEXOIKnAHmDH7qAFoIfsoCWgh+qgBaDH6aAvW4ndyngYe0BN/yQpc+MPt5tVaaPUbPAbSjAjALMKMCMAsyeNxyz5c4JV7ADzCjAjALMKMCMAswowIwCzCjAjALMKKCuk3sCt4j+jZpjpPxz163cYQ8bfOEOfdjgC4I3I3gzgjcjeDOCNyN4M4I3I3gzgjcjeDOCNyN4M4I3I3gzgjcjeLNd/jkqAADo3B8+s2MH7cXf0gAAAABJRU5ErkJggg=='
        
        self.imagem_anterior = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAAh0lEQVRoge3TwQkCMQBE0Y81LFqWJ+3RPVmWYhFagdmAsDPgf5BzhvADkvQPrsB7cG65adsW4Mn38S/gGFs3YWX8+pfctG2mk2Q6KaaTZDpJppNiOkmmk1SRzmGPS1otwINxQqfYuklnxhndc9PmVfyFX5hSC1NqYEoNTKmFKTUwpQamJEm9PohoFvqTHhZTAAAAAElFTkSuQmCC'
        self.imagem_proximo = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAAk0lEQVRoge3TsQ3CMBgF4RMNC0QwFhXsCBVjgZggFZkgjoUi3m/pPimVmxf5DJI0ugfwbXzX3LQ+E/Bi/Qc+wDm2rtOF9i08c9P6mVIFplSBKVVhShWYUgWmVIUpVbB7Soc913U4bpzPf1nxowl4007oFFvXYehHfKM9/p6bts10kkwnyXRSTCfJdJJMJ8V0JGlcC8O+F/rzPPmjAAAAAElFTkSuQmCC'

#Tela_Quadro('igorsantos314',{'Color': 'Red', 'Doing': ['Nenhum'], 'Done': ['Nenhum'], 'On Hold': ['Nenhum'], 'Subtitulo': 'Sensor Solo', 'Titulo': 'Proj2', 'To do': ['Nenhum']})