from tkinter import Tk, Label, Button, Entry,filedialog,Frame, Text
from PIL import Image, ImageTk
import pandas as pd
import webbrowser as web
import pyautogui as pg
import time , re 


class mywindow(Frame):
    
    def __init__(self, master=None):
        super().__init__(master,  bg='#25D366')
        self.master = master
        self.icon = ImageTk.PhotoImage(Image.open("WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\whatsapp_socialnetwork_17360.ico"))
        self.pack()    
        self.master.iconphoto(True, self.icon)
        self.Create_widget()


    def DirArch(self):
        ruta = filedialog.askopenfilename()
        self.Ent.delete(0, 'end')
        self.Ent.insert(0, ruta)

    def update_entry(self,value):
        # Obtiene el contenido actual del Entry
        current_text = self.Tx.get('1.0', 'end')
        # Si el Checkbutton no está seleccionado, no se hace nada
        if not value:
            return
        # Si el contenido del Entry no está vacío, agrega un separador
        if current_text:
            current_text += ", "
        # Agrega el valor del Checkbutton al contenido del Entry
        self.Tx.delete('1.0', 'end')
        self.Tx.insert('1.0', current_text + value)

    def MensPer(self,Nombre, Celular, Otro):
        current_text2 = self.Tx.get('1.0', 'end')
        current_text2 = re.sub(r'\[Nombre\]',Nombre,current_text2)
        current_text2 = re.sub(r'\[Telefono\]',Celular,current_text2)
        current_text2 = re.sub(r'\[Otro\]',Otro,current_text2)
        return current_text2


    
    def Sender(self,DirArc):
        data = pd.read_excel(r"{}".format(DirArc), sheet_name='Ventas')
        for i in range(len(data)):
            celular = data.loc[i,'Celular'].astype(str) # Convertir a string para que se añada al mensaje
            nombre = data.loc[i,'Nombre']
            otro = data.loc[i,'Otro']
                
            # Crear mensaje personalizado
            mensaje = self.MensPer(nombre,celular,otro)
             
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            web.get(chrome_path).open("https://web.whatsapp.com/send?phone=" + celular + "&text=" + mensaje)
                
            time.sleep(30)           # Esperar 30 segundos a que cargue
            pg.click(840,705)      # Hacer click en la caja de texto
            time.sleep(2)           # Esperar 2 segundos 
            pg.press('enter')       # Enviar mensaje 
            time.sleep(3)           # Esperar 3 segundos a que se envíe el mensaje
            pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
            time.sleep(2)




    def Create_widget(self):

        FrameP= Frame(self, bg='#25D366')
        Frame1= Frame(FrameP)
        Frame2= Frame(FrameP)
        Frame3= Frame(FrameP)
        Frame4= Frame(FrameP)
        

        FrameP.pack()
        Frame1.grid(row=0,column=0)
        Frame2.grid(row=1,column=0)
        Frame3.grid(row=2,column=0)
        Frame4.grid(row=3,column=0)


        self.lbl= Label (Frame1,text='Ubicacion de Archivo de Excel:')
        self.btn= Button(Frame1, text='Examinar',  command=self.DirArch)
        self.Ent= Entry(Frame1, width='50',  font=("Arial", 10))
        self.lbl2= Label (Frame2, text='Mensaje a Enviar')
        self.Tx= Text(Frame3,width='100',  height='10', font=("Arial", 10))
        self.btn2= Button(Frame4, text='Aceptar', command=lambda: self.Sender(self.Ent.get()))
        self.btn3 = Button(Frame2, text='Nombre', command=lambda: self.update_entry('[Nombre]'))
        self.btn4 = Button(Frame2, text='Telefono', command=lambda: self.update_entry('[Telefono]'))
        self.btn5 = Button(Frame2, text='Otro', command=lambda: self.update_entry('[Otro]'))

        self.lbl.grid(row=0,column=0)
        self.btn.grid(row=0,column=2)
        self.Ent.grid(row=0,column=1)
        self.btn3.grid(row=0,column=1)
        self.btn4.grid(row=1,column=1)
        self.btn5.grid(row=2,column=1)
        self.lbl2.grid(row=0,column=0, rowspan=3, sticky=('E'))
        self.Tx.pack()
        self.btn2.pack()

root =Tk()
root.wm_title("Mensajes Masivos")
app= mywindow(root)
app.mainloop()
