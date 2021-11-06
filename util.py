import tkinter as tk
import logging
import os.path
import hashlib
from datetime import date

class util:

    def __init__(self) -> None:
        #SETA AS CONFIGURAÇÕES DE LOG
        #logging.basicConfig(filename='log.log', filemode='a', level=logging.DEBUG, format='%(asctime)s::%(levelname)s::%(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p')
        pass
    
    def toCenterScreen(self, width, height):

        root = tk.Tk()

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.destroy()
        
        pos_x = float(screen_width)/2 - width/2
        pos_y = float(screen_height)/2 - height/2
        
        if pos_x < 0:
            pos_x = pos_x * -1

        if pos_y < 0:
            pos_y = pos_y * -1

        return f'{width}x{height}+{pos_x:.0f}+{pos_y:.0f}'

    def generateLog(self, msg, type):

        if type == 'info':
            #ESCREVER EVENTO NO LOG
            logging.info(msg)

        elif type == 'warning':
            #ESCREVER EVENTO NO LOG
            logging.warning(msg)

        elif type == 'error':
            #ESCREVER EVENTO NO LOG
            logging.error(msg)

    def getLog(self):
        log_str = ''

        with open('log.log', 'r') as log:
            for i in log.readlines()[::-1]:
                log_str += i

        return log_str
        
    def validateMachine(self):
        
        if os.path.isfile('C:\Windows\win32_api_config_igtec.dll'):
            return True
    
    def cifrar(self, senha):
        #JOGA A SENHA NA FUNÇÃO DE HASH
        hash =  hashlib.md5(senha.encode())
        
        #RETORNA A SENHA CIFRADA
        return hash.hexdigest()

    def getData(self):
        #PEGA O DIA, MES E ANO ATUAL
        day = date.today().day
        month = date.today().month
        year = date.today().year

        #COLOCA DATA COM DOIS ALGARISMOS
        if len(str(day)) < 2:
            day = f"0{day}"
        
        if len(str(month)) < 2:
            month = f"0{month}"

        #ENVIA A DATA FORMATADA
        return f"{day}/{month}/{year}"

    def validateData(self, data):

        list_data = data.split("/")

        if len(data) < 10:
            return False
        
        if len(list_data) < 3:
            return False
        
        try:
            int(list_data[0])
            int(list_data[1])
            int(list_data[2])

            return True

        except:
            return False
    
    def getColors(self):
        return [
            '#009FE2',
            '#01963F',
            '#E6007D',
            '#F19301',
            '#612678',
            '#FEED02',
            '#FF6347',
            '#00FFFF'
        ]
#print(util().cifrar("13579"))
"""for i in range(50500):
    print(i)
    u.generateLog("TESTE [TESTE] TESTE [TESTE] TESTE [TESTE]", "INFO")"""    
#print(u.cifrar('1234'))
#u.generateLog("Teste", 'warning')


