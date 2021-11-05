from tkinter import *
from tkinter import ttk
from tkinter import font
from typing import List
import base64

from rsa import common
from Persistencia import Persistencia
from util import util
import _thread as th
from beautiful_message import beautiful_message
import copy

class Tela_Quadro:
    
    def __init__(self, usuario, board) -> None:
        
        self.tituloWindow = "IGTEC - BOARD"
        self.tituloWindowAviso = f"{self.tituloWindow} *"

        #print(board)
        self.pilha_board = [copy.deepcopy(board)]
        
        self.board = copy.deepcopy(board)
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
        self.windowQuadro['bg'] = 'White'
        self.windowQuadro.title(self.tituloWindow)
        self.windowQuadro.resizable(False, False)

        #OBEJTOS PARA MENSAGENS
        self.msg = beautiful_message(self.windowQuadro)

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
        self.windowQuadro.bind("<Control-s>", self.salvar)
        self.windowQuadro.bind("<Control-z>", self.ctrlZ)
        
        #FOCAR NA JANELA DE QUADROS
        self.windowQuadro.focus_force()

        self.windowQuadro.mainloop()

    # -- COLUNAS --
    def atualizarTarefas(self, event):
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
    def movePostIt(self, column_atual, postit, column_destino):
        self.adicionarMovido(
            column_destino, 
            postit['Atividade'],
            postit['Color'],
            postit['Data'],
            postit['Prioridade'],
        )

        #print("Tarefa Movida")
        
        #REMOVE A TAREFA
        self.excluirPostItMovido(column_atual, postit)

        #ATUALIZA AS TAREFAS
        self.atualizarTarefas(None)

        #ADICIONAR A ALTERAÇÕES
        self.pilha()

    def excluirPostItMovido(self, column_atual, postit):
        #VARRE O QUADRO ATÉ ENCONTRAR O ID
        for pos, tarefa in enumerate(self.board[column_atual]):
            if tarefa != 'Nenhum':
                if int(tarefa['Id']) == int(postit['Id']):
                    del self.board[column_atual][pos]

        #ATUALIZA AS TAREFAS
        self.atualizarTarefas(None)

    def excluirPostIt(self, column_atual, postit):
        #VARRE O QUADRO ATÉ ENCONTRAR O ID
        for pos, tarefa in enumerate(self.board[column_atual]):
            if tarefa != 'Nenhum':
                if int(tarefa['Id']) == int(postit['Id']):
                    del self.board[column_atual][pos]

        #ATUALIZA AS TAREFAS
        self.atualizarTarefas(None)

        #ADICIONAR A ALTERAÇÕES
        self.pilha()

        #print("Tarefa excluida")

    def exibirPostIts(self):

        #POSIÇÃO INICIAL
        posx = 40

        for postIt in self.board['To do']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameToDo, 'To do', postIt)

        for postIt in self.board['Doing']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameDoing, 'Doing', postIt)

        for postIt in self.board['On Hold']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameOnHold, 'On Hold', postIt)

        for postIt in self.board['Done']:
            if postIt != 'Nenhum':
                self.setPostIt(self.frameDone, 'Done', postIt)

    def setPostIt(self, frame, column, postIt):
        #print(postIt)

        # -- MENU --
        def popup(event):
            menuPopup.post(event.x_root, event.y_root)

        framePostIt = Frame(frame, bg=self.color_theme, width=200, height=90)
        framePostIt.pack(side=TOP, pady=10, padx=5)

        #MENU POPUP
        menuPopup = Menu(framePostIt, font=self.font_msg, fg='Black', bg=postIt['Color'], bd=0, tearoff=0)

        # -- EXIBE A OPÇÃO DE MUDAR PARA A COLUNA QUE NÃO ESTÁ --
        if column != "To do":
            menuPopup.add_command(label="To Do", command=lambda: self.movePostIt(column, postIt, 'To do'))
        
        if column != "Doing":
            menuPopup.add_command(label="Doing", command=lambda: self.movePostIt(column, postIt, 'Doing'))
        
        if column != "On Hold":
            menuPopup.add_command(label="On Hold", command=lambda: self.movePostIt(column, postIt, 'On Hold'))
        
        if column != "Done":
            menuPopup.add_command(label="Done", command=lambda: self.movePostIt(column, postIt, 'Done'))

        menuPopup.add_separator()

        menuPopup.add_command(label="Editar", command=lambda: print(postIt))
        menuPopup.add_command(label="Excluir", command=lambda: self.excluirPostIt(column, postIt, ))

        frFaixa = Frame(framePostIt, height=90, width=10, bg=postIt['Color'])
        frFaixa.place(x=0, y=0)

        lblAtividade = Label(framePostIt, text=self.formatSubtitulo(postIt['Atividade']), font=self.font_menu, bg=self.color_theme, fg='White')
        lblAtividade.place(x=20, y=0)
        
        lblData = Label(framePostIt, text=postIt['Data'], font=self.font_default, bg=self.color_theme, fg='White')
        lblData.place(x=20, y=30)
        
        lblPrioridade = Label(framePostIt, text=postIt['Prioridade'], font=self.font_menu, bg=self.color_theme, fg='White')
        lblPrioridade.place(x=20, y=60)

        def abrir(event):
            print(postIt)
            
        framePostIt.bind("<Button-3>", popup)
        framePostIt.bind("<Double-Button-1>", abrir)

    def formatSubtitulo(self, subtitilo):
        #FORMATA A STRING PARA NÃO UTRAPASSAR A QUANTIDADE DE CARACTERES
        if len(subtitilo) > 16:
            return f"{subtitilo[:16]}..."
        return subtitilo
    
    def voltar(self):
        self.windowQuadro.destroy()

    def novaTarefa(self):

        self.colorTarefa = 'Black'

        self.frameNovaTarefa = Frame(self.windowQuadro, bg='White', width=430, height=370)
        self.frameNovaTarefa.pack(pady=120)
        self.frameNovaTarefa.grab_set()

        #TITULO
        lblTitulo = Label(self.frameNovaTarefa, text='NOVA TAREFA', font=self.font_titulo, bg='White')
        lblTitulo.place(x=120, y=20)

        #ATIVIDADE
        lblAtividade = Label(self.frameNovaTarefa, text='Atividade:', font=self.font_default_labels, bg='White')
        lblAtividade.place(x=10, y=80)

        etAtividade = Entry(self.frameNovaTarefa, font=self.font_default_labels, width=40)
        etAtividade.place(x=10, y=110)

        #DATA
        lblData = Label(self.frameNovaTarefa, text='Data:', font=self.font_default_labels, bg='White')
        lblData.place(x=10, y=150)

        etData = Entry(self.frameNovaTarefa, font=self.font_default_labels, width=10)
        etData.insert(0, util().getData())
        etData.place(x=10, y=180)

        #PRIORIDADE
        lblPrioridade = Label(self.frameNovaTarefa, text='Prioridade:', font=self.font_default_labels, bg='White')
        lblPrioridade.place(x=140, y=150)

        comboPrioridade = ttk.Combobox(self.frameNovaTarefa, font=self.font_default_labels, width=10, state="readonly")

        comboPrioridade['values'] = tuple(
            ['I', 'II', 'III', 'IV', 'V'])
        comboPrioridade.current(0)
        comboPrioridade.place(x=140, y=180)
        
        #COR
        lblCor = Label(self.frameNovaTarefa, text='Cor da Tarefa:', font=self.font_default_labels, bg='White')
        lblCor.place(x=10, y=220)

        #LISTA DE BOTOES
        self.listaBotoesCores = []

        #CRIAR PALETA DE CORES
        posX = 10
        for indice, cor in enumerate(util().getColors()):
            #CRIA CADA BOTÃO COM A COR 
            self.createBotaoCor(indice, posX, cor)

            #ESPAÇAMENTO DE 50 ENTRE OS BOTOES
            posX += 50

        def adicionar():
            
            if len(etAtividade.get().replace(" ", "")) > 0:

                self.adicionar(
                    'To do',
                    etAtividade.get(),
                    self.colorTarefa,
                    etData.get(),
                    comboPrioridade.get()
                )

                #FECHA A JANELA
                fechar()

                #ATUALIZAR CAMPOS
                self.atualizarTarefas(None)
        
        def fechar():
            self.frameNovaTarefa.destroy()

        btSalvar = Button(self.frameNovaTarefa, text='Adicionar', font=self.font_default_labels, fg='White', bg='Black', bd=0, width=9, command= adicionar)
        btSalvar.place(x=10, y=320)

        btSalvar = Button(self.frameNovaTarefa, text='Fechar', font=self.font_default_labels, fg='White', bg='Black', bd=0, width=9, command= fechar)
        btSalvar.place(x=120, y=320)

        #FOCAR NO CAMPO DE ATIVIDADE
        etAtividade.focus_force()

    def createBotaoCor(self, indice, posX, cor):

        def limparSelecao():
            #LIMPA QUALQUER BOTÃO SELECIONADO
            for bt in self.listaBotoesCores:
                bt['bd'] = 0

        def selecionarCor():
            #LIMPA AS SELEÇÕES
            limparSelecao()

            #MUDA A BORDA DO BOTAO SELECIONADO
            self.listaBotoesCores[indice]['bd'] = 2

            #SELECIONA A COR APERTADA
            self.colorTarefa = cor

        #BOTAO COM A COR
        btCor = Button(self.frameNovaTarefa, bg=cor, bd=0, width=5, height=2, command=lambda: selecionarCor())
        btCor.place(x=posX, y=250)

        #ADICIONAR O BOTAO DE COR NA LISTA
        self.listaBotoesCores.append(
            btCor
        )

    def getIdPost(self, column_destino):
        ultima_tarefa = self.board[column_destino][-1]

        print(ultima_tarefa)

        if ultima_tarefa == 'Nenhum':
            return 1

        return int(ultima_tarefa['Id']) + 1

    def adicionarMovido(self, column_destino, atividade, color, data, prioridade):
        #ADICIONAR TAREDA NO BOARD
        self.board[column_destino].append(
            {
                "Id":self.getIdPost(column_destino),
                "Atividade":atividade,
                "Color":color,
                "Data":data,
                "Prioridade":prioridade               
            }
        )

    def adicionar(self, column_destino, atividade, color, data, prioridade):
        #ADICIONAR TAREFA NO BOARD
        self.board[column_destino].append(
            {
                "Id":self.getIdPost(column_destino),
                "Atividade":atividade,
                "Color":color,
                "Data":data,
                "Prioridade":prioridade               
            }
        )

        #ADICIONAR A ALTERAÇÕES
        self.pilha()

    def salvar(self, event):
        #SALVAR ALTERAÇÕES
        Persistencia(self.usuario).salvarAlteracoes(self.board)

        #AVISAR QUE SALVOU
        self.avisoWindow('Salvo')

        #th.start_new_thread(self.msg.destroyMsg, (None,))
        self.msg.msg("info", "ALTERAÇÕES FORAM SALVAS !")

    def pilha(self):
        #ADICIONAR EVENTO NA PILHA
        self.pilha_board.append(
            copy.deepcopy(
                self.board
            )
        )

        #AVISAR QUE NÃO SALVOU
        self.avisoWindow('Pilha')

    def ctrlZ(self, event):
        #print(self.pilha_board)
        if len(self.pilha_board) > 1:
            
            #VOLTA UMA AÇÃO
            self.board = copy.deepcopy(self.pilha_board[-2])

            #REMOVER DA PILHA
            self.pilha_board.pop()

            #ATUALIZA O QUADRO
            self.atualizarTarefas(None)

            #VOLTOU
            print("VOLTOU")

    def avisoWindow(self, event):

        if event == 'Pilha':
            #AVISAR QUE AS ALTERAÇÕES NÃO FORAM SALVAS
            self.windowQuadro.title(self.tituloWindowAviso)

        elif event == 'Salvo':
            #RETIRAR AVISO DO TITULO DA JANELA
            self.windowQuadro.title(self.tituloWindow)

    def setImagensBase64(self):
        self.imagem_menu = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAABkUlEQVR4nO3awS5DQRTG8W+wrETtxLpWZUsEb8QzEI/gpTSSEu2KrdhhwVL7t2g0chW3qTkj+v22Pcl89yQ393RmJDMzM7MAwAFwBbzy2StwCeyXzpkFsAo8TXjwqkegGZVrIWohSduSVmrUNSXtZM4yFtmARqbamUQ24E9yA0oHKM0NCFzrforau2wpSgGWgE6NOeAcWIrKlaIWkiSgIelQ0pakxcrPA0nXks5SSi+RuczMzOZU6BwgScCGpLYmzwH9lNJNdKYwwCkw/GYKHAInpXNmAWz88PAfm9CKyhX5Z6iteq9ckrSZOctYZAOq7/xv1c7E+wGlA5TmBgSuNchUO5PIBvQlUaMOSb3MWcoATmoMQseRmUqMwi2NvvOTRuFeSuk2OpOZmdmcij4aW5Z0pK+3xHoaHY09R+YKwehw9KLGjlCHwMPRMMBejYd/txuVK/LP0NoUtevZUlR4P6B0gNLcgNIBSotswDTXXv7fFRlGl6Ufa3wCHwi8LB0K2Ae6fH1dvgvslc5pZmZm8+EN6vTRQDQnGnkAAAAASUVORK5CYII='

#Tela_Quadro('igorsantos314',{'Color': 'Red', 'Doing': ['Nenhum'], 'Done': ['Nenhum'], 'On Hold': ['Nenhum'], 'Subtitulo': 'Sensor Solo', 'Titulo': 'Proj2', 'To do': ['Nenhum']})