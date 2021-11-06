from tkinter import *
from tkinter import ttk
import base64
from time import sleep
from tkinter import font
from typing import List
from Persistencia import Persistencia
from Tela_Novo_Quadro import Tela_Novo_Quadro
from Tela_Quadro import Tela_Quadro
from beautiful_message import beautiful_message
from util import util
import _thread as th

class Tela_Home:
    
    def __init__(self, usuario) -> None:
        
        #USUARIO LOGADO
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
        self.windowMain = Tk()
        self.windowMain.geometry(util().toCenterScreen(985, 600))
        self.windowMain['bg'] = 'White'
        self.windowMain.title("IGTEC - KANBANBOARD")
        self.windowMain.resizable(False, False)

        imagem_usuario = PhotoImage(data=base64.b64decode(self.imagem_usuario))
        self.lblusuario = Label(self.windowMain, image=imagem_usuario, bg=self.color_contrast)
        self.lblusuario.image = imagem_usuario
        self.lblusuario.place(x=0, y=0)

        lblBemVindo = Label(self.windowMain, text='Bem vindo,', font=self.font_default, bg=self.color_contrast)
        lblBemVindo.place(x=70, y=5)
        
        self.lblUsuario = Label(self.windowMain, text=self.usuario, font=self.font_usuario, bg=self.color_contrast)
        self.lblUsuario.place(x=70, y=30)

        # -- TITULO --
        imagem_kanban = PhotoImage(data=base64.b64decode(self.imagem_kanban))
        self.lblKanban = Label(self.windowMain, text='IGTEC KABAN BOARD', font=self.font_titulo, image=imagem_kanban, compound=LEFT, bg=self.color_contrast)
        self.lblKanban.image = imagem_kanban
        self.lblKanban.pack(pady=40)

        # -- MENU --
        def popup(event):
            self.menuPopup.post(event.x_root-270, event.y_root)
        
        #MENU POPUP
        self.menuPopup = Menu(self.windowMain, font=self.font_default, fg='Black', bg='White', bd=0, tearoff=0)
        self.menuPopup.add_command(label="Novo Quadro", command=lambda: self.novoQuadro())
        self.menuPopup.add_command(label="Novo Quadro Compartilhado", command=lambda: 'imprimir(None)')
        self.menuPopup.add_separator()
        self.menuPopup.add_command(label="Sair", command=lambda: self.windowMain.destroy())
        
        imagem_menu = PhotoImage(data=base64.b64decode(self.imagem_menu))
        btMenu = Button(self.windowMain, image=imagem_menu, bd=0, height=60, width=30, bg=self.color_contrast)
        btMenu.image = imagem_menu
        btMenu.place(x=950, y=0)

        #BUSCAR EVENTO DE CLICK SOBRE O BOTÃO
        btMenu.bind("<Button-1>", popup)

        # -- MEUS QUADROS --
        width_frame = 960
        height_frame = 450

        main_frame = Frame(self.windowMain, bg='White', width=width_frame, height=height_frame)
        main_frame.place(x=0, y=144)

        my_canvas = Canvas(main_frame, bg='White', bd=0, width=width_frame, height=height_frame)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e:my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        self.frameMeusQuadros = Frame(my_canvas, bg=self.color_contrast, height=150, width=width_frame)
        self.frameMeusQuadros.place(x=0, y=200)

        my_canvas.create_window((0,0), window=self.frameMeusQuadros, anchor="nw")
        
        lblMeusQuadros = Label(self.frameMeusQuadros, text='Meus Quadros', font=self.font_titulo, bg=self.color_contrast)
        lblMeusQuadros.place(x=10, y=10)

        #INCLUIR TODOS OS QUADROS NO FRAME
        self.adicionarMeusQuadros()

        # -- QUADROS COMPARTILHADOS --
        """lblQuadrosCompartilhados = Label(self.windowMain, text='Quadros Compartilhados', font=self.font_titulo, bg=self.color_contrast)
        lblQuadrosCompartilhados.place(x=10, y=320)

        self.frameCompartilhados = Frame(self.windowMain, bg=self.color_contrast, height=110, width=830)
        self.frameCompartilhados.place(x=10, y=370)"""

        #FOCAR NA JANELA
        self.windowMain.focus_force()

        self.windowMain.mainloop()

    def novoQuadro(self):
        #FECHAR JANELA
        self.windowMain.destroy()

        #ABRIR JANELA DE CRIAR NOVO QUADRO
        Tela_Novo_Quadro(self.usuario)

        #REABRE A TELA NOVAMENTE
        Tela_Home(self.usuario)

    def adicionarMeusQuadros(self):
        #POSIÇÃO INICIAL
        posx = 10
        posy = 60

        contTarefasLinha = 0

        #PEGA TODOS OS QUADRO DO USUARIO
        quadros = Persistencia(self.usuario).getBoards()

        #print(len(quadros))
        
        #VARRE A LISTA DE QUADROS
        for board in quadros:

            #IGNORA LOGIN E SENHA
            if "Senha" not in board:
                if contTarefasLinha > 4:

                    #ADICIONA O ESPAÇAMENTO DE MAIS UMA LINHA DO FRAME
                    self.frameMeusQuadros['height'] += 100

                    posx = 10
                    posy += 100

                    contTarefasLinha = 0

                self.createQuadro(posx, posy, board)
                
                #ESPAÇAMENTO ENTRE QUADROS
                posx += 190

                #
                contTarefasLinha += 1

    def abrirQuadro(self, board):

        #APAGAR JANELA
        self.windowMain.destroy()
        
        #ABRIR QUADRO
        Tela_Quadro(self.usuario, board)

        #REABRIR A JANELA
        Tela_Home(self.usuario)

    def createQuadro(self, posx, posy, board):
        #FRAME PRINCIPAL
        frameMiniQuadro = Frame(self.frameMeusQuadros, bg=self.color_theme, width=180, height=90)
        frameMiniQuadro.place(x=posx, y=posy)
        
        #FRAME DA BARRA LATERAL COLORIDA
        frameFaixa = Frame(frameMiniQuadro, bg=board["Color"], width=10, height=90)
        frameFaixa.place(x=0, y=0)
        
        btTituloQuadro = Button(frameMiniQuadro, text=board["Titulo"], bd=0, bg=self.color_theme, fg='White', font=self.font_usuario, command=lambda: self.abrirQuadro(board))
        btTituloQuadro.place(x=10, y=0)
        
        lblSubtituloQuadro = Label(frameMiniQuadro, text=self.formatSubtitulo(board["Subtitulo"]), bd=0, bg=self.color_theme, fg='White', font=self.font_default)
        lblSubtituloQuadro.place(x=15, y=45)
        
    def adicionarCompartilhados(self):
        posx = 40
        for i in range(4):
            frameMiniQuadro = Frame(self.frameCompartilhados, bg=self.color_theme, width=180, height=90)
            frameMiniQuadro.place(x=posx, y=10)

            posx += 190

    def formatSubtitulo(self, subtitilo):
        #FORMATA A STRING PARA NÃO UTRAPASSAR A QUANTIDADE DE CARACTERES
        if len(subtitilo) > 16:
            return f"{subtitilo[:16]}..."
        return subtitilo

    def setImagensBase64(self):
        self.imagem_usuario = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAAEf0lEQVR4nO3bX4hWRRjH8Y9rllC6mpoFuW1/F7GorjK7qNAu666LMrEiSiiSoIiCKItAoj8oJEEXlRFkRUFQUd3URV0UkaTZZn+3wIz1X7p2YeV2MWdxW99z3vfMnHPW8P3Cc/Ge9535Pc+cM2dmnpmXLl26dDmOmdKg1nxciAGchVk4JftuBPswhG+xFb836Fst9OAabMA3GC1p2/AslmZ1/W+Yh0fxq/JB59kvWIO5DcZRmtl4Wnicqwp8oo3gSaH7HDNMwUqhz9YV+ETbiRVNBNeOmdikucAn2lvCkzcpLMKPbRxswn7AwppjPYol2J3g9N/4Cu9ktiW7FlvfLiyuNeJxLMHBSEd/w93CSDGR07Ba6N8xdY9ooBEWib/zbzgy8SliBt6M1Nilxu4wS3yff0G5WecUvBSp9T16o6MscCj2rnyBEyM0T8KXkZqvRegVsjLSkVFcnaC7LEF3eYLuf5gtfpLzdQX6g5HaO3UwY+xkkfGQ8IaO4b3IcuN5N7LcfDyYKj4HB8Q/hqtSHcCdCfoj2iyg2j0Bq3U2dOUxklB2jD8Syp6Mu4p+UNQAPbg5QZz4rjOeMxLL36IgzqIGWIoFieKXJJaHixPL9+HKmIIbxPe9MdstjOexTMfeCvxYHyMeO/xMtHtixDPuq8iHLWWFT69IeBR7cH5ZB4Tk6b6KfDis5PtoaUXCYzao3PukT8gOV+lDyxlp3ktwoISznTCAz3BtB7+9Dp/jghp8OIoTcn7cX7E4oVu9jU/wCj4Wsr2EO34VbsLlNWjD2a0u5jXAzJqcgCsya5oZrS7mdYGU2d+xSqkGOG7Ia4Aq5vDHGgdaXcxrgP01OjJZtIwprwGGanRksvi51cW8Bhis0ZHJomVMecPgVmH2VOX5gd3YLGSWf8o+j/XLGULioh/n4FKcWqH2qIj03DZpU8+d2IgbxU2s+oXE5kbxmyXRiyHC4YSyQgczh5epdojtyep8GX9G+LUuRrRMSvpgJpKavemEeVir3PZcVEKkR5irt6v8U5wbG00CffioA/+GJDyNa9pU/lRK5RUwFc+08Gu8PZwiMFf+kZcXNXvKLI+ifcT92owm7e7eLjyX892CDso3QQ/OzPlug5CRSmKW/GHosdTKK+BxrX3bocJl/YockcO4vSqRCFZlPrTy7YaqxV7PEfoHt1Yt1gG3yQ/+1ToEe4UDSXlPwlrhrVw3U/FEjh+j2K7GjNZC4cWYJ/6+cA64LvrxYYH+sOoTukexWPFp0BHcK+zqVMV0YZOkSPcALqtQs5DFip+EUeFE2P3SVnVz8ID2i6FhDQY/xkLhQFK7qeghoWvcIWx0Tiuoc5qwoboKH+CvDurfLuGxT53J9eJ5XF+izCF8J2x77c2uzc7sPOUOVG0ShuFJT+EtFx75dnerKtuhhnE+lV5heEo5UtPO9gvDbZ0bN8nMwSPCMrSqwIeEVV2VabLa6RF2ZNc7kmPs1A5nZdYJyYzaFl1NLmfn4SJh17dPuJvj/zS1R0jAjP1parhB37p06dLl+ORfOBG/whDjMksAAAAASUVORK5CYII='
        
        self.imagem_menu = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAAgElEQVRoge3WSw5AQBBF0cvqiP1vQNsHAzGhI0RTwT1JjTqpz6TzQJK+pgMGYFxVAtrAvQ5LbJdfqi89rCrdkHnRx2bWJZtF8IBodxww7LylG+YV15L/iXqgCdxLkl7CNHqGaTSaB0QzjWaYRiXpEtPoGabRaB4QzTSaYRqV9CMT0ZxFqQgirw4AAAAASUVORK5CYII='
        
        self.imagem_kanban = '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'
        self.imagem_kanban2 = 'iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAABmJLR0QA/wD/AP+gvaeTAAAB8ElEQVR4nO3cS07DMBSF4cNjCyyEWTpjdyyIQTtjwmJYBTCoLEWiVZrUN8fX/j/JwxTnHLt5IJAAAAAAAAAwiif3BDY6SHqR9O2eyGgmSR+SfiV9mucylHnw8/HmnNQIrgVfBrsgyFLw7IIga4JnF1S0JXh2QQUHSSdtD76M970nnt29K76ML7H6VyF4E4I3IXiTSdJR9wd/0vlCXdtB0mvA59q1vuK7fZeUKfj5SP+1ljX4MtLuguzBp94FNS6uR51Dqm3Lk3W6XZB9xaffBdlX/KWR6l1SDys+en6hnCt+Up0VH/WAF3HO/yydXFTwLT9Zz+cXbukka2r9q6bM70cx53/RHgVkDL6LAjIHn7qAHoJPWUBPwacqoMfg0xTQ8rukGre74e6dQG8rfogCMgTfZQGZgu+qgIzBd1NAqxfXYQqoaY8VTwEXOIKnAHmDH7qAFoIfsoCWgh+qgBaDH6aAvW4ndyngYe0BN/yQpc+MPt5tVaaPUbPAbSjAjALMKMCMAsyeNxyz5c4JV7ADzCjAjALMKMCMAswowIwCzCjAjALMKKCuk3sCt4j+jZpjpPxz163cYQ8bfOEOfdjgC4I3I3gzgjcjeDOCNyN4M4I3I3gzgjcjeDOCNyN4M4I3I3gzgjcjeLNd/jkqAADo3B8+s2MH7cXf0gAAAABJRU5ErkJggg=='
        
        self.imagem_anterior = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAAh0lEQVRoge3TwQkCMQBE0Y81LFqWJ+3RPVmWYhFagdmAsDPgf5BzhvADkvQPrsB7cG65adsW4Mn38S/gGFs3YWX8+pfctG2mk2Q6KaaTZDpJppNiOkmmk1SRzmGPS1otwINxQqfYuklnxhndc9PmVfyFX5hSC1NqYEoNTKmFKTUwpQamJEm9PohoFvqTHhZTAAAAAElFTkSuQmCC'
        self.imagem_proximo = 'iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAAk0lEQVRoge3TsQ3CMBgF4RMNC0QwFhXsCBVjgZggFZkgjoUi3m/pPimVmxf5DJI0ugfwbXzX3LQ+E/Bi/Qc+wDm2rtOF9i08c9P6mVIFplSBKVVhShWYUgWmVIUpVbB7Soc913U4bpzPf1nxowl4007oFFvXYehHfKM9/p6bts10kkwnyXRSTCfJdJJMJ8V0JGlcC8O+F/rzPPmjAAAAAElFTkSuQmCC'

#Tela_Home('igorsantos314')