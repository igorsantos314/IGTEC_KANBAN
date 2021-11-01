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

    def insertServico(self, nome, endereco, contato, data, hora, categoria, subcategoria1, subcategoria2, valor_servico, valor_material, desconto, pagamento, obs):
        #PEGA O ULTIMO ID
        id = self.getId()

        # ADIDIONA VALOR NO DICIONÁRIO
        data_service = {
            'id': id,
            'nome': nome,
            'endereco': endereco,
            'contato': contato,
            'data': data,
            'hora': hora,
            'categoria': categoria,
            'subcategoria1': subcategoria1,
            'subcategoria2': subcategoria2,
            'valor_servico': valor_servico,
            'valor_material': valor_material,
            'desconto': desconto,
            'pagamento': pagamento,
            'obs': obs
            }

        # SALVAR NO DICIONARIO
        self.db.child("Servicos").child(id).set(data_service)

    def getTipoServicos(self):
        #PEGA OS TIPO DO FIREBASE
        list_tipos_servicos = self.db.child("TipoServicos").get().each()

        #RETORNA A LISTA DOS TIPOS DE SERVIÇOS
        return [tipo.val() for tipo in list_tipos_servicos]

    def getSubcategorias(self, categoria):
        #PEGA AS SUBCATEGORIAS DO FIREBASE
        list_subcategorias = self.db.child("Subcategoria1").child(categoria).get().each()

        if list_subcategorias == None:
            return []

        #RETORNA A LISTA DE SUBCATEGORIAS
        return [tipo.val() for tipo in list_subcategorias]

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