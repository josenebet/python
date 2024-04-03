import tkinter as tk
from tkinter import ttk
import sqlite3



class mywindow5(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.icon = ImageTk.PhotoImage(Image.open("WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\whatsapp_socialnetwork_17360.ico"))
        self.id_alimento=None
        #self.master.iconphoto(True, self.icon)        
        self.Create_widget()

    def llenar_listbox(self,event):
        self.listbox.delete(0,tk.END)
        for i in self.entry:
            i.delete(0,tk.END)
        valor=event.widget.get()
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        # Consulta para obtener el plato y los ingredientes de la receta con id 1
        consulta=("""
        SELECT  INGREDIENTES,CANTIDADES
        FROM RECETAS
        WHERE PLATO = ?
        """)
        cursor.execute(consulta, (valor,))
        receta = cursor.fetchone()
        lista = list(receta)
        for i in range(len(lista)):
            lista[i] = lista[i].split(",")
        for i in lista[0]:
            self.listbox.insert(tk.END,i)
        for j,i in enumerate(lista[1]):
            self.entry[j].insert(0,i)          
    
    def Create_widget(self):
        FrameP=tk.Frame(self)
        FrameP.pack()
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT PLATO FROM RECETAS")
        alimentos = cursor.fetchall()
        conexion.close() 
        alimentos = list(map(lambda x: x[0], alimentos))
        alimentos = [alimento.strip("{}") for alimento in alimentos]            
        combobox=ttk.Combobox(FrameP,values=alimentos)
        lbl1=tk.Label(FrameP,text='Ingredientes')
        lbl2=tk.Label(FrameP,text='Cant')
        self.listbox=tk.Listbox(FrameP)
        combobox.grid(row=0,column=0,columnspan=2)
        lbl1.grid(row=1,column=0)
        lbl2.grid(row=1,column=1)
        
        self.listbox.grid(row=2,column=0,rowspan=8)
        self.entry=[]
        for i in range(8):
            self.entry.append(tk.Entry(FrameP,width=5))
            self.entry[i].grid(row=i+2,column=1)

        combobox.bind("<<ComboboxSelected>>", self.llenar_listbox)

 

'''if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(1,0)
    root.mainloop()'''