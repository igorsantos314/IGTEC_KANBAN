import pyrebase

class Persistencia:

    def __init__(self):

        self.config_service_system = {
            "apiKey": "AIzaSyCLui161fjs2Mf9kT3RePfg_fIKIQOcMAo",
            "authDomain": "igtec-service-system.firebaseapp.com",
            "databaseURL": "https://igtec-service-system-default-rtdb.firebaseio.com",
            "projectId": "igtec-service-system",
            "storageBucket": "igtec-service-system.appspot.com",
            "messagingSenderId": "809625755875",
            "appId": "1:809625755875:web:0da0d0b7ad6c3e527865d6"
        };

        firebase = pyrebase.initialize_app(self.config_service_system)
        self.db = firebase.database()

    def getId(self):
        service_id = self.db.child("Servicos").get().each()

        if service_id == None:
            return 0

        return len(service_id)

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