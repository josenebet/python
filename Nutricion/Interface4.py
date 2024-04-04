import tkinter as tk
from tkinter import ttk
import sqlite3


class mywindow4(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.icon = ImageTk.PhotoImage(Image.open("WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\whatsapp_socialnetwork_17360.ico"))
        self.id_alimento=None
        #self.master.iconphoto(True, self.icon)        
        self.Create_widget()

    def guardar_elemento_bd(self,tabla,datos):
        valores=[]
        for i in datos:
            valores.append(i.get())        
        for i in range(3,8):
            valores[i]=float(valores[i])
        valores.append(self.id_alimento)
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        consulta = """
        UPDATE TABLA_NUTRICIONAL
        SET Tipo=?, Alimento=?, Coccion=?,
            Calorias=?, grCarb=?, grProt=?,
            grGrasa=?, Fibra=?
        WHERE "index"=?
            """
        cursor.execute(consulta, valores)
        conexion.commit()
        conexion.close()
        lista_alimentos=self.listar()
        lista_alimentos.reverse()
        tabla.delete(*tabla.get_children())
        for p in lista_alimentos:
            tabla.insert('',0, text=str(p[0]),values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]))
        for i in datos:
            i.delete(0,tk.END)
            i.config(state='disabled')

    def editar_elemento(self,tabla,entry):
        self.id_alimento=tabla.item(tabla.selection())['text'] 
        for j, i in enumerate(entry):
            i.config(state='normal')
            i.insert(0,str(tabla.item(tabla.selection())['values'][j]))

    def borrar_elemento_bd(self,tabla):    
        self.id_alimento=tabla.item(tabla.selection())['text'] 
        plato=tabla.item(tabla.selection())['values'][1]
        print(plato)
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        consulta = f"""
        DELETE FROM TABLA_NUTRICIONAL
        WHERE "index" = ?
            """ 
        cursor.execute(consulta, (self.id_alimento,))
        conexion.commit()
        conexion.close()
        lista_alimentos=self.listar()
        lista_alimentos.reverse()
        tabla.delete(*tabla.get_children())
        for p in lista_alimentos:
            tabla.insert('',0, text=str(p[0]),values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]))

        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        consulta = f"""
        DELETE FROM RECETAS
        WHERE Plato = ?
            """ 
        cursor.execute(consulta, (plato,))
        conexion.commit()
        conexion.close()

    def listar(self):
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT * FROM TABLA_NUTRICIONAL')        
        lista_alimentos =[]
        lista_alimentos =  cursor.fetchall()
        conexion.commit()
        conexion.close()        
        return lista_alimentos
    
    def Create_widget(self):
        FrameP= tk.Frame(self)
        FrameP.pack()
        frame,lblf1,entf1=[],[],[]
        txtlabels=['Tipo:','Alimento:','Coccion:','Calorias','Hidratos de Carb:','Proteinas:','Grasa:','Fibra:']
        for i in range(3):
            frame.append(tk.Frame(FrameP))
            frame[i].grid(row=i,column=0)
        #frame 1
        for j,i in enumerate(txtlabels):
            lblf1.append(tk.Label(frame[0],text=i))
            entf1.append(tk.Entry(frame[0],state='disabled'))
            if j< 3:
                lblf1[j].grid(row=j,column=0)
                entf1[j].grid(row=j,column=1)
            elif j< 6:
                lblf1[j].grid(row=j-3,column=2)
                entf1[j].grid(row=j-3,column=3)
            else: 
                lblf1[j].grid(row=j-6,column=4)
                entf1[j].grid(row=j-6,column=5)

        #frame 2
        btnf1=[]
        textbtn=['Editar','Eliminar','Guardar']
        for j,i in enumerate(textbtn):
            btnf1.append(ttk.Button(frame[1],text=i,width=25))
            btnf1[j].grid(row=0,column=j)        

        #frame 3
        lista_alimentos= self.listar()
        lista_alimentos.reverse()
        tabla=ttk.Treeview(frame[2],column=('Tipo:','Alimento:','Coccion:','Calorias','Hidratos de Carb:','Proteinas:','Grasa:','Fibra:'))
        tabla.grid(row=0,column=0,sticky='nse')
        scroll=ttk.Scrollbar(frame[2],orient='vertical',command=tabla.yview)
        scroll.grid(row=0,column=1,sticky='nse')
        tabla.configure(yscrollcommand=scroll.set)
        tabla.heading('#0',text='ID')
        tabla.column('#0', width=80)
        for j,i in enumerate (txtlabels):
            tabla.heading(f'#{j+1} ',text=i)
            tabla.column(f'#{j+1}', width=100)

        for p in lista_alimentos:
            tabla.insert('',0, text=str(p[0]),values=(p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]))
        
        btnf1[0].config(command= lambda : self.editar_elemento(tabla,entf1))
        btnf1[1].config(command= lambda : self.borrar_elemento_bd(tabla))
        btnf1[2].config(command= lambda : self.guardar_elemento_bd(tabla,entf1))

