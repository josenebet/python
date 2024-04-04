import pandas as pd
import webbrowser as web
import pyautogui as pg
import time
import openpyxl


data = pd.read_excel(r'C:\Users\User\Documents\python\WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\Clientes.xlsx', sheet_name='Ventas')
for i in range(len(data)):
    celular = data.loc[i,'Celular'].astype(str) # Convertir a string para que se añada al mensaje
    nombre = data.loc[i,'Nombre']
    producto = data.loc[i,'Producto']
        
    # Crear mensaje personalizado
    mensaje = "Hola, " + nombre + "! Gracias por comprar " + producto + " con nosotros 🙌"
        
        # Abrir una nueva pestaña para entrar a WhatsApp Web
        # Opción 1: Si te abre WhastApp Web directamente en Google Chrome
    #     web.open("https://web.whatsapp.com/send?phone=" + celular + "&text=" + mensaje)
        
        # Opción 2: Si te abre WhastApp Web en Microsoft Edge, especificar que lo abra en Chrome
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    web.get(chrome_path).open("https://web.whatsapp.com/send?phone=" + celular + "&text=" + mensaje)
        
    time.sleep(30)           # Esperar 8 segundos a que cargue
    pg.click(840,705)      # Hacer click en la caja de texto
    time.sleep(2)           # Esperar 2 segundos 
    pg.press('enter')       # Enviar mensaje 
    time.sleep(3)           # Esperar 3 segundos a que se envíe el mensaje
    pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
    time.sleep(2)

