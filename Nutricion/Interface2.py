import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from reportlab.platypus import Table, SimpleDocTemplate,TableStyle,Paragraph,Image
from reportlab.lib.pagesizes import letter
import sqlite3


class mywindow2(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.icon = ImageTk.PhotoImage(Image.open("WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\whatsapp_socialnetwork_17360.ico"))
        #self.master.iconphoto(True, self.icon)        
        self.Create_widget()        
    
    def Filtrar_Listbox(self,event):
        #Funcion para colocar valores en un listbox de acuerdo al valor de un combobox
        valor=event.widget.get()
        self.listbox1.delete(0,tk.END)
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        consulta = """
        SELECT Alimento,Coccion 
        FROM TABLA_NUTRICIONAL
        WHERE Tipo = ?
        """
        cursor.execute(consulta, (valor,))
        fila = cursor.fetchone()
        alimentos = []
        for fila in cursor.fetchall():
            alimento_completo = f"{fila[0]} {fila[1]}"
            alimentos.append(alimento_completo)
        for lista in alimentos:
           self.listbox1.insert(tk.END,lista)
        conexion.close() 

    def crear_labl_tabla(self,indice):
        #uncion para crear una tabla de labels
        for j in range(5):
            for i in range(7):
                self.dict[indice][j+2][i].grid(row=i+1, column=j+2)
                self.dict[indice][j+2][i+7].grid(row=i+1, column=j+2)
                self.dict[indice][j+2][i+19].grid(row=i+1, column=j+2)
            for i in range(5):
                self.dict[indice][j+2][i+14].grid(row=i+1, column=j+2)                                                
    
    def llenar_tabla_suma(self,relativo,relativoListBox,listbox,event):
        value= float(event.widget.get())
        dato = listbox.get(relativoListBox)
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        consulta = """
        SELECT CALORIAS,grCarb,grProt,grGrasa,Fibra 
        FROM TABLA_NUTRICIONAL
        WHERE ALIMENTOCOCCION = ?
        """
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute(consulta, (dato,))
        dffila = cursor.fetchone()
        
        Calorias = round((value/100)*float(dffila[0]),2)
        HCarb = round((value/100)*float(dffila[1]),2)
        Proteina = round((value/100)*float(dffila[2]),2)
        Fibra = round((value/100)*float(dffila[4]),2)
        Grasa = round((value/100)*float(dffila[3]),2)             
        listAux=[Calorias,HCarb,Proteina,Grasa,Fibra]
        for i in range(len(listAux)):
            self.dict[self.indice_dia_sem1][i+2][relativo]['text']=str(listAux[i])

        suma =[0] * 5
        suma1 = [0] * 5
        suma2 =[0] * 5 
        suma3 = [0] * 5
        
        for i in range (5):
            for j in range(7):
                suma[i]+=float(self.dict[self.indice_dia_sem1][i+2][j].cget('text'))
                suma1[i]+=float(self.dict[self.indice_dia_sem1][i+2][j+7].cget('text'))
                suma3[i]+=float(self.dict[self.indice_dia_sem1][i+2][j+19].cget('text'))
        for i in range (5):
            for j in range(5):
                suma2[i]+=float(self.dict[self.indice_dia_sem1][i+2][j+14].cget('text'))
        
        for i in range(5):
            self.dict[self.indice_dia_sem1][7][i]['text']=str(round(suma[i],2))
            self.dict[self.indice_dia_sem1][7][i+5]['text']=str(round(suma1[i],2))
            self.dict[self.indice_dia_sem1][7][i+10]['text']=str(round(suma2[i],2))
            self.dict[self.indice_dia_sem1][7][i+15]['text']=str(round(suma3[i],2))
        
        self.crear_labl_tabla(self.indice_dia_sem1)
        self.actualizar_graficos_PIE()
        self.actualizar_graficos_BARRA()

    def actualizar_graficos_BARRA(self):
        sumCalorias, sumHC, sumProt, sumGrasa=0,0,0,0
        for i in [0,5,10,15]:
            sumCalorias+=(float(self.dict[self.indice_dia_sem1][7][i].cget('text'))/float(self.lblframe11[9].cget('text')))*100
            sumHC+=(float(self.dict[self.indice_dia_sem1][7][i+1].cget('text'))/ float(self.lblframe11[11].cget('text')))*100
            sumProt+=(float(self.dict[self.indice_dia_sem1][7][i+2].cget('text'))/float(self.lblframe11[13].cget('text')))*100
            sumGrasa+=(float(self.dict[self.indice_dia_sem1][7][i+3].cget('text'))/float(self.lblframe11[15].cget('text')))*100
        
        x = 0.5 + np.arange(4)        
        y = [sumCalorias, sumHC, sumProt, sumGrasa]
        label='C','H','P','G'
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))  
        plt.rcParams.update({'figure.autolayout': True})
        self.axbar.clear()
        self.axbar.barh(x, y, align='center',color=colors)
        self.axbar.set_yticks(x,labels=label)
        self.axbar.set_title('Consumo Diario')
        self.axbar.set_xlim([0,120])
        self.axbar.invert_yaxis()
        self.axbar.axvline(100, ls='--', color='r')        
        self.figbar.canvas.draw()
        plt.close(self.figbar)
    
    def actualizar_graficos_PIE(self):
        datos = [[float(self.dict[self.indice_dia_sem1][7][i+1].cget('text')) + 0.0001 for i in range(3)],
                 [float(self.dict[self.indice_dia_sem1][7][i+5].cget('text')) + 0.0001 for i in range(3)],
                  [float(self.dict[self.indice_dia_sem1][7][i+11].cget('text')) + 0.0001 for i in range(3)],
                    [float(self.dict[self.indice_dia_sem1][7][i+16].cget('text')) + 0.0001 for i in range(3)],]
                
        labels='Hidratos','Proteina','Grasa'
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(datos[0])))
        plt.rcParams.update({'figure.autolayout': True}) 
        for i in range (len(self.dict_fig[self.indice_dia_sem1])-1):
            self.dict_fig[self.indice_dia_sem1][i+1].clear()
            self.dict_fig[self.indice_dia_sem1][i+1].pie(datos[i], colors=colors, labels=labels, autopct='%.0f%%',textprops={'size':'smaller'},radius=1.1,wedgeprops={"linewidth": 1, "edgecolor": "white"})
                
        self.dict_fig[self.indice_dia_sem1][1].set_title('Composicion Desayuno')
        self.dict_fig[self.indice_dia_sem1][2].set_title('Composicion Almuerzo')
        self.dict_fig[self.indice_dia_sem1][3].set_title('Composicion Merienda')
        self.dict_fig[self.indice_dia_sem1][4].set_title('Composicion Cena')
       
        self.dict_fig[self.indice_dia_sem1][0].canvas.draw()       

    def insertar_datos_listbox(self,event):
        dato = self.listbox1.get(self.listbox1.curselection()[0])
        
        if self.comb2.get()=='Desayuno':
            self.dict[self.indice_dia_sem1][1][0].insert(tk.END, dato)
        elif self.comb2.get()=='Almuerzo':
            self.dict[self.indice_dia_sem1][1][1].insert(tk.END, dato)
        elif self.comb2.get()=='Merienda':
            self.dict[self.indice_dia_sem1][1][2].insert(tk.END, dato)  
        else:
            self.dict[self.indice_dia_sem1][1][3].insert(tk.END, dato)

    def borrar_datos_listbox(self,event):
        indice=event.widget.curselection()
        event.widget.delete (indice,indice)
        
        if event.widget is self.dict[self.indice_dia_sem1][1][0]:
            for i in range(indice[0],self.dict[self.indice_dia_sem1][1][0].size()):
                self.dict[self.indice_dia_sem1][0][i].delete(0,tk.END)
                self.dict[self.indice_dia_sem1][0][i].insert(0,self.dict[self.indice_dia_sem1][0][i+1].get())
            self.dict[self.indice_dia_sem1][0][self.dict[self.indice_dia_sem1][1][0].size()].delete(0,tk.END)
            
        elif event.widget is self.dict[self.indice_dia_sem1][1][1]:
            for i in range(indice[0],self.dict[self.indice_dia_sem1][1][1].size()):
                self.dict[self.indice_dia_sem1][0][i+7].delete(0,tk.END)
                self.dict[self.indice_dia_sem1][0][i+7].insert(0,self.dict[self.indice_dia_sem1][0][i+8].get())
            self.dict[self.indice_dia_sem1][0][self.dict[self.indice_dia_sem1][1][1].size()+7].delete(0,tk.END)
        elif event.widget is self.dict[self.indice_dia_sem1][1][2]:
            for i in range(indice[0],self.dict[self.indice_dia_sem1][1][2].size()):
                self.dict[self.indice_dia_sem1][0][i+14].delete(0,tk.END)
                self.dict[self.indice_dia_sem1][0][i+14].insert(0,self.dict[self.indice_dia_sem1][0][i+15].get())
            self.dict[self.indice_dia_sem1][0][self.dict[self.indice_dia_sem1][1][2].size()+14].delete(0,tk.END)
        else:
            for i in range(indice[0],self.dict[self.indice_dia_sem1][1][3].size()):
                self.dict[self.indice_dia_sem1][0][i+19].delete(0,tk.END)
                self.dict[self.indice_dia_sem1][0][i+19].insert(0,self.dict[self.indice_dia_sem1][0][i+20].get())
            self.dict[self.indice_dia_sem1][0][self.dict[self.indice_dia_sem1][1][0].size()+19].delete(0,tk.END)
    
    def generar_hojas_notebook(self,diasem,indice):
        p1 = ttk.Frame(self.notebook)
        self.notebook.add(p1, text=diasem)

        #Generar Frames necesarios
        frameEnP1,framef1p1=[],[]
        
        for i in range (2):
            frameEnP1.append(tk.Frame(p1))
            frameEnP1[i].grid(row=0,column=i)
        
        for j in range (4):
            framef1p1.append(tk.Frame(frameEnP1[0]))
            framef1p1[j].grid(column=0,row=j)

        #Labels que dicen Cantidad
        lblcant=[]
        for i,j in enumerate(framef1p1):
            lblcant.append(tk.Label(j,text='Cantidad'))
            lblcant[i].grid(row=0,column=0)   

        #Generar Entrys del primer frame
        filas_des_alm_cen=7
        filas_merienda=5
        columnas_tabla=5
        for container in framef1p1:
            if container==framef1p1[2]:
                for i in range (filas_merienda):
                    self.dict[indice][0].append(tk.Entry(container,width=5))    
            else:
                for i in range(filas_des_alm_cen):
                    self.dict[indice][0].append(tk.Entry(container,width=5))

        for i in range(filas_des_alm_cen):
            self.dict[indice][0][i].grid(row=i+1,column=0)
            self.dict[indice][0][i+7].grid(row=i+1,column=0)
            self.dict[indice][0][i+19].grid(row=i+1,column=0)       
        for i in range(filas_merienda):
            self.dict[indice][0][i+14].grid(row=i+1,column=0)
        
        #generar Labels vacios para espacio
        lblvacio=[]
        for container in framef1p1:
            lblvacio.append(tk.Label(container))
        
        lblvacio[0].grid(row=8,column=0)
        lblvacio[1].grid(row=8,column=0)
        lblvacio[2].grid(row=6,column=0)
        lblvacio[3].grid(row=8,column=0)         
        #Generar Labels qu van en el top de los listbox del segundo frame   
        lblntb1=tk.Label(framef1p1[0],text='Desayuno')
        lblntb2=tk.Label(framef1p1[1],text='Almuerzo')
        lblntb3=tk.Label(framef1p1[3],text='Cena')
        lblntb4=tk.Label(framef1p1[2],text='Merienda')
        #Generar que dicen total
        lbltot=[]
        for container in framef1p1:
            lbltot.append(tk.Label(container,text='Total'))        
        #Generar listbox del segundo frame
        self.dict[indice][1].append(tk.Listbox(framef1p1[0],height=8,width=22, font=("Arial", 10)))
        self.dict[indice][1].append(tk.Listbox(framef1p1[1],height=8,width=22, font=("Arial", 10)))
        self.dict[indice][1].append(tk.Listbox(framef1p1[2],height=6,width=22, font=("Arial", 10)))
        self.dict[indice][1].append(tk.Listbox(framef1p1[3],height=8,width=22, font=("Arial", 10)))
        
        lblntb1.grid(row=0,column=1)
        lblntb2.grid(row=0,column=1)
        lblntb3.grid(row=0,column=1)
        lblntb4.grid(row=0,column=1)

        for i in range (4):
            if i == 2:
                self.dict[indice][1][i].grid(row=1,column=1,rowspan=5)
            else:self.dict[indice][1][i].grid(row=1,column=1,rowspan=7)
        for i in range (len(lbltot)):
            if i == 2:
                lbltot[i].grid(row=6,column=1)
            else: lbltot[i].grid(row=8,column=1)
        
        #generar elementos de la tabla de componentes
        lblCompAlim=[]
        for container in framef1p1:           
            lblCompAlim.append(tk.Label(container, text='Calorias'))
            lblCompAlim.append(tk.Label(container, text='Hidratos de Carb'))
            lblCompAlim.append(tk.Label(container, text='Proteinas'))
            lblCompAlim.append(tk.Label(container, text='Grasa'))
            lblCompAlim.append(tk.Label(container, text='Fibra'))
        
        for i in range (columnas_tabla):
            lblCompAlim[i].grid(row=0,column=i+2)
            lblCompAlim[i+5].grid(row=0,column=i+2)
            lblCompAlim[i+10].grid(row=0,column=i+2)
            lblCompAlim[i+15].grid(row=0,column=i+2)

        for container in framef1p1:
            for i in range(columnas_tabla):
                self.dict[indice][7].append(tk.Label(container,text='0',font=('Arial',8)))
        
        for i in range(columnas_tabla):
            self.dict[indice][7][i].grid(row=8,column=i+2)
            self.dict[indice][7][i+5].grid(row=8,column=i+2)
            self.dict[indice][7][i+10].grid(row=6,column=i+2)
            self.dict[indice][7][i+15].grid(row=8,column=i+2)

        for j in range(columnas_tabla):
            for container in framef1p1:
                if container==framef1p1[2]:
                    for i in range (filas_merienda):
                        self.dict[indice][j+2].append(tk.Label(container,text='0',width=10, font=('Arial',8)))    
                else:
                    for i in range(filas_des_alm_cen):
                        self.dict[indice][j+2].append(tk.Label(container,text='0',width=10,font=('Arial',8)))

        self.crear_labl_tabla(indice)

        x = [1,1,1]
        labels='Hidratos','Proteina','Grasa'
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))
        plt.rcParams.update({'figure.autolayout': True})        
        fig, (ax,ax2,ax3,ax4) = plt.subplots(4,figsize=(2.5,6))
        self.dict_fig[indice].extend([fig, ax, ax2, ax3, ax4])
        for i in range (len(self.dict_fig[indice])-1):
            self.dict_fig[indice][i+1].pie(x, colors=colors, labels=labels, textprops={'size':'smaller'},radius=1.1,wedgeprops={"linewidth": 1, "edgecolor": "white"})
        self.dict_fig[indice][1].set_title('Composicion Desayuno')
        self.dict_fig[indice][2].set_title('Composicion Almuerzo')
        self.dict_fig[indice][3].set_title('Composicion Merienda')
        self.dict_fig[indice][4].set_title('Composicion Cena')
        canvas1 = FigureCanvasTkAgg(self.dict_fig[indice][0],frameEnP1[1])
        canvas1.get_tk_widget().grid(row=0,column=0)
        plt.close(self.dict_fig[indice][0])
        
        self.listbox1.bind("<Double-Button-1>", self.insertar_datos_listbox)
        for i in range(len(self.dict[indice][1])):
            self.dict[indice][1][i].bind("<Double-Button-1>", self.borrar_datos_listbox)      
           
        self.dict[indice][0][0].bind("<Return>", lambda event: self.llenar_tabla_suma(0,0,self.dict[indice][1][0],event))
        self.dict[indice][0][1].bind("<Return>", lambda event: self.llenar_tabla_suma(1,1,self.dict[indice][1][0],event))
        self.dict[indice][0][2].bind("<Return>", lambda event: self.llenar_tabla_suma(2,2,self.dict[indice][1][0],event))
        self.dict[indice][0][3].bind("<Return>", lambda event: self.llenar_tabla_suma(3,3,self.dict[indice][1][0],event))
        self.dict[indice][0][4].bind("<Return>", lambda event: self.llenar_tabla_suma(4,4,self.dict[indice][1][0],event))
        self.dict[indice][0][5].bind("<Return>", lambda event: self.llenar_tabla_suma(5,5,self.dict[indice][1][0],event))
        self.dict[indice][0][6].bind("<Return>", lambda event: self.llenar_tabla_suma(6,6,self.dict[indice][1][0],event))
        self.dict[indice][0][7].bind("<Return>", lambda event: self.llenar_tabla_suma(7,0,self.dict[indice][1][1],event))
        self.dict[indice][0][8].bind("<Return>", lambda event: self.llenar_tabla_suma(8,1,self.dict[indice][1][1],event))
        self.dict[indice][0][9].bind("<Return>", lambda event: self.llenar_tabla_suma(9,2,self.dict[indice][1][1],event))
        self.dict[indice][0][10].bind("<Return>", lambda event: self.llenar_tabla_suma(10,3,self.dict[indice][1][1],event))
        self.dict[indice][0][11].bind("<Return>", lambda event: self.llenar_tabla_suma(11,4,self.dict[indice][1][1],event))
        self.dict[indice][0][12].bind("<Return>", lambda event: self.llenar_tabla_suma(12,5,self.dict[indice][1][1],event))
        self.dict[indice][0][13].bind("<Return>", lambda event: self.llenar_tabla_suma(13,6,self.dict[indice][1][1],event))
        self.dict[indice][0][14].bind("<Return>", lambda event: self.llenar_tabla_suma(14,0,self.dict[indice][1][2],event))
        self.dict[indice][0][15].bind("<Return>", lambda event: self.llenar_tabla_suma(15,1,self.dict[indice][1][2],event))
        self.dict[indice][0][16].bind("<Return>", lambda event: self.llenar_tabla_suma(16,2,self.dict[indice][1][2],event))
        self.dict[indice][0][17].bind("<Return>", lambda event: self.llenar_tabla_suma(17,3,self.dict[indice][1][2],event))
        self.dict[indice][0][18].bind("<Return>", lambda event: self.llenar_tabla_suma(18,4,self.dict[indice][1][2],event))
        self.dict[indice][0][19].bind("<Return>", lambda event: self.llenar_tabla_suma(19,0,self.dict[indice][1][3],event))
        self.dict[indice][0][20].bind("<Return>", lambda event: self.llenar_tabla_suma(20,1,self.dict[indice][1][3],event))
        self.dict[indice][0][21].bind("<Return>", lambda event: self.llenar_tabla_suma(21,2,self.dict[indice][1][3],event))
        self.dict[indice][0][22].bind("<Return>", lambda event: self.llenar_tabla_suma(22,3,self.dict[indice][1][3],event))
        self.dict[indice][0][23].bind("<Return>", lambda event: self.llenar_tabla_suma(23,4,self.dict[indice][1][3],event))
        self.dict[indice][0][24].bind("<Return>", lambda event: self.llenar_tabla_suma(24,5,self.dict[indice][1][3],event))
        self.dict[indice][0][25].bind("<Return>", lambda event: self.llenar_tabla_suma(25,6,self.dict[indice][1][3],event))
    
    def evento_pestaña_cambiada(self,event):                 
        self.indice_dia_sem1 = str( self.notebook.index(tk.CURRENT))
        self.actualizar_graficos_BARRA()
    
    def insertar_menu_base_datos(self,my_data):
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS MENU (
            CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE TEXT,
            CEDULA TEXT,
            TABLA_MENU TEXT                                   
        )
        """)
        conexion.commit()
        conexion.close()

        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO MENU (NOMBRE, CEDULA, TABLA_MENU)
            VALUES (?, ?, ?)
        """,(self.lblframe11[1].cget('text'),self.lblframe11[3].cget('text'),my_data))

        conexion.commit()
        conexion.close()

    def create_table_pdf(self):
        keys_diasemana=["0", "1",'2','3','4','5','6']
        dic_menu = {
                    "alimentos": {
                        "0": [[], [], [], []],
                        "1": [[], [], [], []],
                        "2": [[], [], [], []],
                        "3": [[], [], [], []],
                        "4": [[], [], [], []],
                        "5": [[], [], [], []],
                        "6": [[], [], [], []],
                    },
                    "cantidades": {
                        "0": [[], [], [], []],
                        "1": [[], [], [], []],
                        "2": [[], [], [], []],
                        "3": [[], [], [], []],
                        "4": [[], [], [], []],
                        "5": [[], [], [], []],
                        "6": [[], [], [], []],
                    },
                }
        for dia in keys_diasemana:
           for i,k in enumerate ([-1,6,13,18]):
               for j in range (self.dict[dia][1][i].size()):
                    k+=1
                    dic_menu["alimentos"][dia][i].append(self.dict[dia][1][i].get(j))
                    dic_menu["cantidades"][dia][i].append(self.dict[dia][0][k].get())
                    
        suma=0
        for dia in keys_diasemana:
            suma+=max(len(dic_menu["cantidades"][dia][0]),len(dic_menu["cantidades"][dia][1]),len(dic_menu["cantidades"][dia][2]),len(dic_menu["cantidades"][dia][3]))
        data_rows=[]
        for i in range (suma):
           data_rows.append([' ',' ',' ',' ',' ',' ',' ',' ',' ',])
         
        sumadias=0
        aux1,aux2=0,0
        for dia in keys_diasemana:            
            sumadias = max(len(dic_menu["cantidades"][dia][0]),len(dic_menu["cantidades"][dia][1]),len(dic_menu["cantidades"][dia][2]),len(dic_menu["cantidades"][dia][3]))
            aux2+=sumadias 
                  
            if sumadias!=0:
                for i in range (aux1,aux2):
                        data_rows[i][0]=('Dia: '+str(int(dia)+1))
            for i,k in enumerate(dic_menu["cantidades"][dia][0]):
                data_rows[i+aux1][1]=k
            for i,k in enumerate(dic_menu["alimentos"][dia][0]):
                data_rows[i+aux1][2]=k             
            for i,k in enumerate(dic_menu["cantidades"][dia][1]):
                    data_rows[i+aux1][3]=k
            for i,k in enumerate(dic_menu["alimentos"][dia][1]):
                    data_rows[i+aux1][4]=k
            for i,k in enumerate(dic_menu["cantidades"][dia][2]):
                    data_rows[i+aux1][5]=k
            for i,k in enumerate(dic_menu["alimentos"][dia][2]):
                    data_rows[i+aux1][6]=k
            for i,k in enumerate(dic_menu["cantidades"][dia][3]):
                data_rows[i+aux1][7]=k
            for i,k in enumerate(dic_menu["alimentos"][dia][3]):
                    data_rows[i+aux1][8]=k
            aux1+=sumadias
                  
        header_row = [['Dia de la Semana', 'Cant', 'Desayuno', 'Cant', 'Almuerzo', 'Cant', 'Merienda', 'Cant', 'Cena'],]
        my_data=[]
        my_data = header_row +data_rows
        self.insertar_menu_base_datos(my_data)
        return(my_data)
    
    def create_PDF(self):
       
       my_doc=SimpleDocTemplate(self.lblframe11[1].cget('text')+'.pdf',pagesize=letter)
       t=Table(self.create_table_pdf())
       t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, 'black'),
        ('BOX', (0, 0), (-1, -1), 0.25, 'black'),
     ]))
       texto_titulo =  ('<br />''<br />'+self.lblframe11[0].cget('text')+  self.lblframe11[1].cget('text')
                        +'<br />'+self.lblframe11[2].cget('text')+self.lblframe11[3].cget('text')+'<br /><br /><br /><br />')
       p = Paragraph(texto_titulo)
       i=Image('images/logo.png',width=100,height=100)
       elements=[]
       elements.append(i)
       elements.append(p)       
       elements.append(t)
       my_doc.build(elements)

    def buscar_datos_base_datos(self):
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
        SELECT * FROM PACIENTES
        ORDER BY CODIGO DESC
        LIMIT 1
        """)
        fila = cursor.fetchone()
        fila2=fila[1:]
        j=0
        for i in range(len (fila2)):
            j+=1
            self.lblframe11[i+j]['text']=fila2[i]
        conexion.close()

    
    def Create_widget(self):

        FrameP= tk.Frame(self)
        FrameP.pack()

        Frame1= tk.Frame(FrameP)
        Frame2= tk.Frame(FrameP)
        Frame3= tk.Frame(FrameP)

        Frame1.grid(row=0,column=0)
        Frame2.grid(row=0,column=1)
        Frame3.grid(row=0,column=2)

               
        #SEGUNDO FRAME PRINCIPAL
        
        self.LBL1=tk.Label(Frame2,text='Opciones del Menu:')
        self.comb1 = ttk.Combobox(Frame2, values=['Hidrato','Proteina','Grasa'])
        self.comb2 = ttk.Combobox(Frame2, values=['Desayuno','Almuerzo','Merienda','Cena'])
        self.listbox1= tk.Listbox(Frame2,height=37,width=22, font=('Arial',10))
        scroll=ttk.Scrollbar(Frame2,orient='vertical',command=self.listbox1.yview)
        self.listbox1.configure(yscrollcommand=scroll.set)

        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ALIMENTOCOCCION FROM TABLA_NUTRICIONAL")
        alimentos = cursor.fetchall()
        conexion.close() 
        alimentos = list(map(lambda x: x[0], alimentos))
        alimentos = [alimento.strip("{}") for alimento in alimentos]            
        for lista in alimentos:
           self.listbox1.insert(tk.END,lista)
        
        
        self.LBL1.grid(row=0,column=0,columnspan=2)
        self.comb1.grid(row=2,column=0,columnspan=2)
        self.comb2.grid(row=1,column=0,columnspan=2)
        self.listbox1.grid(row=3,column=0,sticky='nse')
        scroll.grid(row=3,column=1,sticky='nse')
        self.comb1.bind("<<ComboboxSelected>>", self.Filtrar_Listbox)

        #PRIMER FRAME PRINCIPAL
        
        Frame11=tk.Frame(Frame1)
        Frame12=tk.Frame(Frame1)
        Frame11.grid(row=0,column=0)
        Frame12.grid(row=1,column=0)
        self.lblframe11=[]
        textlblftrame11=['Nombre:',' ','CI:',' ','Edad:',' ','IMC:','0','GET:','0','GET Hidratos de Carb:','0',
                       'GET Proteina:','0','GET Grasa:','0']
        for i in textlblftrame11:
            self.lblframe11.append(tk.Label(Frame11,text=i))
        j=0
        k=-1
        for i in range (8):
            j+=1
            k+=1
            self.lblframe11[i+k].grid(row=i,column=0)
            self.lblframe11[i+j].grid(row=i,column=1)
        
        btn1=tk.Button(Frame11,text=('Generar PDF'),command= self.create_PDF)
        btn1.grid(row=8,column=0,columnspan=2)

        self.buscar_datos_base_datos()

        x = 0.5 + np.arange(4)
        y = [0, 0, 0, 0]
        label='C','H','P','G'
        colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))  
        plt.rcParams.update({'figure.autolayout': True})
        self.figbar, self.axbar = plt.subplots(figsize=(3.5,3))
        self.axbar.barh(x, y, align='center',color=colors)
        self.axbar.set_yticks(x,labels=label)
        self.axbar.set_title('Consumo Diario')
        self.axbar.set_xlim([0,120])
        self.axbar.invert_yaxis()  
        self.axbar.axvline(100, ls='--', color='r')    
        canvas1 = FigureCanvasTkAgg(self.figbar,Frame12)
        canvas1.get_tk_widget().grid(row=0,column=0)
        plt.close(self.figbar)
        
        #TERCER FRAME PRINCIPAL
        self.notebook = ttk.Notebook(Frame3)
        self.notebook.pack()
        self.indice_dia_sem1 = '0'
        keys_diasemana=["0", "1",'2','3','4','5','6']
        self.dict=dict.fromkeys(keys_diasemana)
        self.dict_fig=dict.fromkeys(keys_diasemana)
        for dia in keys_diasemana:
            self.dict[dia] = []
            self.dict_fig[dia]=[]
            for i in range(8):
                self.dict[dia].append([]) 
        # Agregar pestañas al Notebook
        for i, diasem in enumerate(["Lunes", "Martes",'Miercoles','Jueves','Viernes','Sabado','Domingo']):
            self.generar_hojas_notebook(diasem, str(i))               

        self.notebook.bind("<<NotebookTabChanged>>",  self.evento_pestaña_cambiada)
                   

    
'''if __name__ == "__main__":
    root = tk.Tk()
    root.mainloop()'''