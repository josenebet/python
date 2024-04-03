import tkinter as tk
from tkinter import ttk
import sqlite3
import re

class mywindow3(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.icon = ImageTk.PhotoImage(Image.open("WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\whatsapp_socialnetwork_17360.ico"))
             
        #self.master.iconphoto(True, self.icon)        
        self.Create_widget()
    
    def obtener_ultimo_valor(self):        
        conexion = sqlite3.connect('mibasedatos.db')
        cursor = conexion.cursor()
        # Crea la consulta SQL con ORDER BY y LIMIT
        consulta = """
            SELECT "index"
            FROM TABLA_NUTRICIONAL
            ORDER BY "index" DESC
            LIMIT 1
        """
        # Ejecuta la consulta
        cursor.execute(consulta)
        # Obtiene el resultado
        valor = cursor.fetchone()[0]
        # Cierra la conexión
        conexion.close()
        return valor
    
    def insert_base_datos1(self,data):
        ultimo_valor = self.obtener_ultimo_valor()+1
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO TABLA_NUTRICIONAL ("index",Tipo,Alimento,Coccion, Calorias ,grCarb,grProt,grGrasa,Fibra,ALIMENTOCOCCION )
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """,(ultimo_valor,data[0][0].get(),data[1].get(),data[0][1].get(),float(data[2][0].get()),float(data[2][1].get()),
             float(data[2][2].get()),float(data[2][3].get()),float(data[2][4].get()),data[1].get()+' '+data[0][1].get()))
        conexion.commit()
        conexion.close()
        for i in data[2]:
            i.delete(0,'end')        
        for i in data[0]:
            i.delete(0,'end')

    def insert_base_datos2(self,data):
        ultimo_valor = self.obtener_ultimo_valor()+1
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO TABLA_NUTRICIONAL ("index",Tipo,Alimento,Coccion, Calorias , grCarb,grProt,grGrasa,Fibra,ALIMENTOCOCCION)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """,(ultimo_valor,'Plato',data[0].get(),data[2].get(),float(data[1][0].cget('text')),float(data[1][1].cget('text')),
             float(data[1][2].cget('text')),float(data[1][3].cget('text')),float(data[1][4].cget('text')),data[0].get()+' '+data[2].get()))
        conexion.commit()
        conexion.close()
        self.insert_base_datos3([data[0],data[3],data[4]])
        for i in data[3]:
            i.delete(0,'end')
        data[4].delete(0,'end')
        data[0].delete(0,'end')

    def insert_base_datos3(self,data):
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS RECETAS (
            CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
            PLATO TEXT,
            INGREDIENTES TEXT,
            CANTIDADES INT
        )
        """)
        conexion.commit()
        conexion.close()
        ingredientes = []
        cantidades = []
        for item in data[2].get(0, 'end'):
            ingredientes.append(item)
        for entry in data[1]:
            cantidades.append(entry.get())
                
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
        INSERT INTO RECETAS (PLATO , INGREDIENTES, CANTIDADES )
                    VALUES (?,?,?)
        """,(data[0].get(), ",".join(ingredientes), ",".join(cantidades)))
        conexion.commit()
        conexion.close()

    def insertar_datos_listbox(self,l1,l2,event):
        dato = l1.get(l1.curselection()[0])
        l2.insert(tk.END, dato)

    def borrar_datos_listbox(self,entry,event):
        indice=event.widget.curselection()
        event.widget.delete (indice,indice)

        for i in range(indice[0],event.widget.size()):
                entry[i].delete(0,tk.END)
                entry[i].insert(0,entry[i+1].get())
        entry[event.widget.size()].delete(0,tk.END)

    def calc_agregados(self,l1,label,entry,entry2,event):
        lista=l1.get(0, 'end')
        TOTCal,TOThc,TOTprot,TOTgras,TOTfib=0,0,0,0,0
        for i, valor in enumerate(lista):
            conexion = sqlite3.connect("mibasedatos.db")
            cursor = conexion.cursor()
            consulta = """
            SELECT CALORIAS,grCarb,grProt,grGrasa,Fibra 
            FROM TABLA_NUTRICIONAL
            WHERE ALIMENTOCOCCION = ?
            """
            cursor.execute(consulta, (valor,))
            fila = cursor.fetchone()
            TOTCal+=round(float(entry[i].get())*fila[0]/100,2)
            TOThc+=  round(float(entry[i].get())*fila[1]/100,2)
            TOTprot+=round(float(entry[i].get())*fila[2]/100,2)
            TOTgras+=round(float(entry[i].get())*fila[3]/100,2)
            TOTfib+= round(float(entry[i].get())*fila[4]/100,2)
            label[0]['text']=str(TOTCal)
            label[1]['text']=str(TOThc)
            label[2]['text']=str(TOTprot)
            label[3]['text']=str(TOTgras)
            label[4]['text']=str(TOTfib)
            label[5]['text']=str(round(TOTCal/float(entry2.get()),2))
            label[6]['text']=str(round(TOThc/float(entry2.get()),2))
            label[7]['text']=str(round(TOTprot/float(entry2.get()),2))
            label[8]['text']=str(round(TOTgras/float(entry2.get()),2))
            label[9]['text']=str(round(TOTfib/float(entry2.get()),2))
        conexion.commit()
        conexion.close()      

    def create_notebook(self):
        p1 = ttk.Frame(self.notebook)
        p2 = ttk.Frame(self.notebook)
        self.notebook.add(p1, text='Ingrediente')
        self.notebook.add(p2, text='Plato')

        Frame,Frame2=[], []
        for i in range(2):
            Frame.append(tk.Frame(p1))
            Frame[i].grid(row=0,column=i)
        Frame.append(tk.Frame(p1))
        Frame[2].grid(row=1,column=0,columnspan=2)
        for i in range(5):
            Frame2.append(tk.Frame(p2))
        Frame2[0].grid(row=0,column=0)
        Frame2[1].grid(row=0,column=1)
        Frame2[2].grid(row=0,column=2)
        Frame2[3].grid(row=1,column=0,columnspan=3)
        Frame2[4].grid(row=2,column=0,columnspan=3)

        #Frame 1 de la primera pestaña
        lblf1,lblf2=[],[]
        lbltext=['Tipo:','Coccion:','Alimento:','Calorias:','Hidratos de Carb:','Proteinas:','Grasas:','Fibras:'
                 ,'0','0','0','0','0','0','0','0','0','0']
        for i in range(3):
            lblf1.append(tk.Label(Frame[0],text=lbltext[i]))
            lblf1[i].grid(row=i,column=0)

        combf1=[]
        value=[['Hidrato','Proteina','Grasa'],['Crudo','Hervido','Horneado','Asado','En Aceite']]
        for i in range(2):
            combf1.append(ttk.Combobox(Frame[0],values=value[i],width=16))
        entryf1=tk.Entry(Frame[0],width=19)

        combf1[0].grid(row=0,column=1)
        combf1[1].grid(row=1,column=1)
        entryf1.grid(row=2,column=1)

        #Frame 2 de la primera pestaña
        entryf2=[]
        for i in range(5):
            lblf2.append(tk.Label(Frame[1],text=lbltext[i+3]))
            lblf2[i].grid(row=i,column=0)
        
        for i in range(5):
            entryf2.append(tk.Entry(Frame[1], width=4))
            entryf2[i].grid(row=i,column=1)

        #Frame 3 de la primera pestaña
        btnf1=ttk.Button(Frame[2],text='Agregar',command= lambda: self.insert_base_datos1([combf1,entryf1,entryf2,]))
        btnf1.pack()

        #Frame 1 de la segunda pestaña
        lblf1p2=tk.Label(Frame2[0], text='Alimento:').pack()
        listboxf1p2=tk.Listbox(Frame2[0],width=22)                
        listboxf1p2.pack()
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ALIMENTO, COCCION FROM TABLA_NUTRICIONAL")
        alimentos = []
        for fila in cursor.fetchall():
            alimento_completo = f"{fila[0]} {fila[1]}"
            alimentos.append(alimento_completo)
        for lista in alimentos:
           listboxf1p2.insert(tk.END,lista)
        conexion.close()
               
       #Frame 2 de la segunda pestaña
        lblf1p2=tk.Label(Frame2[1], text='Plato:')
        entryf2p2=tk.Entry(Frame2[1], width=16)
        listboxf2p2=tk.Listbox(Frame2[1], width=22) 
        lblf1p2.grid(row=0,column=0)
        entryf2p2.grid(row=0,column=1)
        listboxf2p2.grid(row=1,column=0,rowspan=8,columnspan=2)
        listboxf1p2.bind("<Double-Button-1>", lambda event: self.insertar_datos_listbox(listboxf1p2,listboxf2p2,event))
                
        entryf3p2=[]
        lblf3p2=tk.Label(Frame2[1], text='Cant')
        lblf3p2.grid(row=0,column=2)
        for i in range(8):
            entryf3p2.append(tk.Entry(Frame2[1],width=5))
            entryf3p2[i].grid(row=i+1,column=2)
        listboxf2p2.bind("<Double-Button-1>", lambda event:self.borrar_datos_listbox(entryf3p2,event))
       
        #Frame 4 de la segunda pestaña
        lblf4p2=[]
        for i in range(len(lbltext)-3):
            lblf4p2.append(tk.Label(Frame2[3],text=lbltext[i+3]))
            if i <5:
                lblf4p2[i].grid(row=i,column=0)
            elif i<10:lblf4p2[i].grid(row=i-5,column=1)
            else:lblf4p2[i].grid(row=i-10,column=2)
        lblf4p22=tk.Label(Frame2[3],text='Porcion:')
        lblf4p23=tk.Label(Frame2[3],text='Coccion:')
        entryf4p2=tk.Entry(Frame2[3],width=4)  
        combf4p2=ttk.Combobox(Frame2[3],values=value[1],width=10)
        lblf4p22.grid(row=0,column=3)
        entryf4p2.grid(row=0,column=4)
        lblf4p23.grid(row=1,column=3)
        combf4p2.grid(row=1,column=4)

        for i in entryf3p2:
            i.bind("<Return>", lambda event: self.calc_agregados(listboxf2p2,lblf4p2[5:],entryf3p2,entryf4p2,event))
                
        #Frame 5 de la segunda pestaña
        btnf5p2=ttk.Button(Frame2[4],text='Agregar',command= lambda: self.insert_base_datos2([entryf2p2,lblf4p2[10:],combf4p2,entryf3p2,listboxf2p2]))
        btnf5p2.pack()
    
    def Create_widget(self):
        FrameP= tk.Frame(self)
        FrameP.pack()
        self.notebook = ttk.Notebook(FrameP)
        self.notebook.pack()
        self.create_notebook()


'''if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(0,0) 
    root.mainloop()'''