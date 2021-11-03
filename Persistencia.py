import pyrebase

class Persistencia:

    def __init__(self, usuario):
    
        self.usuario = usuario

        self.config_kanban_board = {
            "apiKey": "AIzaSyCXVVpAcc-mc4RbSfCdRPbAvuHhJdWsrY8",
            "authDomain": "igtec-kanbanboard.firebaseapp.com",
            "databaseURL": "https://igtec-kanbanboard-default-rtdb.firebaseio.com",
            "projectId": "igtec-kanbanboard",
            "storageBucket": "igtec-kanbanboard.appspot.com",
            "messagingSenderId": "343804134483",
            "appId": "1:343804134483:web:983b6b01f230d84c4432a6",
            "measurementId": "G-MM9DVC9ZBN"
        }

        firebase = pyrebase.initialize_app(self.config_kanban_board)
        self.db = firebase.database()

    def getId(self):
        service_id = self.db.child(self.usuario).get().each()

        if service_id == None:
            return 0

        return len(service_id)

    def getIdTarefa(self, board, coluna):
        tarefa_id = self.db.child(self.usuario).child(board).child(coluna).get().each()

        if tarefa_id == None:
            return 0

        return len(tarefa_id)

    def existTarefa(self, board, coluna, atividade):
        #PEGA OS TIPO DO FIREBASE
        if self.db.child(self.usuario).child(board).child(coluna).child(atividade).get().each():
            return True
        return False

    def existUsuario(self):
        #PEGA OS TIPO DO FIREBASE
        if self.db.child(self.usuario).get().each():
            return True
        return False

    def createBoard(self, titulo, subtitulo, color):
        
        data_board_main = {
                    titulo:{
                        "Titulo":titulo,
                        "Subtitulo":subtitulo,
                        "Color":color,
                        "To do":["Nenhum"],
                        "Doing":["Nenhum"],
                        "On Hold":["Nenhum"],
                        "Done":["Nenhum"]
                    }
                }

        if not self.existUsuario():
            print("Cliente não existe")
            data_board = {
                self.usuario: data_board_main
            }
        
            self.db.set(data_board)

        else:
            self.db.child(self.usuario).update(data_board_main)
        
    def getBoards(self):
        #PEGA OS TIPO DO FIREBASE
        list_boards = self.db.child(self.usuario).get().each()

        #RETORNA A LISTA DOS TIPOS DE SERVIÇOS
        return [board.val() for board in list_boards]
    
    def getBoard(self, board):
        #PEGA OS TIPO DO FIREBASE
        current_board = self.db.child(self.usuario).child(board).get().each()

        data_board = {}

        for i in current_board:
            data_board[i.key()] = i.val()

        #RETORNA A LISTA DE TODAS AS TAREFAS
        return data_board

    def adicionarTarefas(self, board, atividade, color, data, prioridade, coluna='To do'):
        
        data_tarefa = {
            self.getIdTarefa(board, coluna):{
                "Atividade":atividade,
                "Color":color,
                "Data":data,
                "Prioridade":prioridade               
            }
        }

        self.db.child(self.usuario).child(board).child(coluna).update(data_tarefa)

#print(Persistencia("igorsantos314").getBoard("Proj2"))
#Persistencia("igorsantos314").adicionarTarefas("Proj Kanban", "Algo", "White", "02/11/2021", "IV")
#Persistencia("igorsantos314").createBoard("Proj Kanban", "Quadro kanban", "Yellow")
#Persistencia("igorsantos314").createBoard("Proj2", "Sensor Solo", "Red")

#print(Persistencia().getTipoServicos())
"""Persistencia().insertServico(
    'igor',
    'água fria',
    '81 98233074',
    '30/10/2021',
    '19:18',
    'unha',
    '--',
    '--',
    25,
    0,
    0,
    'DINHEIRO',
    '--'
)"""