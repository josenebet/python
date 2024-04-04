import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import sqlite3
import re
from Interface2 import mywindow2
from Interface3 import mywindow3
from Interface4 import mywindow4
from Interface5 import mywindow5

class mywindow(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        #self.icon = ImageTk.PhotoImage(Image.open("WhatsApp-Bulk-and-Customized-Messages-Without-Saving-Contacts-main\whatsapp_socialnetwork_17360.ico"))
        #self.master.iconphoto(True, self.icon)
        self.Create_widget()
        self.create_menu_window()

    def abrir_ventana1(self):
        toplevel = tk.Toplevel(self.parent)
        mywindow2(toplevel).pack(side="top", fill="both", expand=True)
        toplevel.title('Creacion de Menu')

    def abrir_ventana2(self):
        toplevel = tk.Toplevel(self.parent)
        mywindow3(toplevel).pack(side="top", fill="both", expand=True)
        toplevel.title('Añadir a Base de Datos')
        toplevel.resizable(0,0) 
    
    def abrir_ventana3(self):
        toplevel = tk.Toplevel(self.parent)
        mywindow4(toplevel).pack(side="top", fill="both", expand=True)
        toplevel.title('Editar Base de Datos')
        toplevel.resizable(0,0)
    
    def abrir_ventana4(self):
        toplevel = tk.Toplevel(self.parent)
        mywindow5(toplevel).pack(side="top", fill="both", expand=True)
        toplevel.title('Receta de Platos')
        toplevel.resizable(1,0)

    def nuevo_paciente(self):
        pass

    def crear_labl_tabla(self):
        for i in range(len(self.list_lbl_tabla)):
            for j in range(len(self.list_lbl_tabla[0])):    
                self.entry = tk.Label(self.FrameTreeview, background='white', relief='ridge', width=20)
                self.entry.grid(row=i+1, column=j+2)
                self.entry.config(text=self.list_lbl_tabla[i][j])    
    
    def llenar_tabla(self,valor_combo_box, relativo, event):
        value= float(event.widget.get())
        value2=valor_combo_box.get()  
                      
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        consulta = """
        SELECT CALORIAS,grCarb,grProt,grGrasa,Fibra 
        FROM TABLA_NUTRICIONAL
        WHERE ALIMENTOCOCCION = ?
        """
        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute(consulta, (value2,))
        fila2 = cursor.fetchone()

        Calorias = round(((value/100)*float(fila2[0])/self.GET2)*100,2)
        HCarb = round(((value/100)*float(fila2[1])/self.GETcarbo)*100,2)
        Proteina = round(((value/100)*float(fila2[2])/self.GETProteina)*100,2)
        Fibra = round((value/100)*float(fila2[4]),2)
        Grasa = round(((value/100)*float(fila2[3])/self.GETGrasa)*100,2)             
        listAux=[Calorias,HCarb,Proteina,Grasa,Fibra]
        for i in range(len(self.list_lbl_tabla[0])):
            self.list_lbl_tabla[relativo][i]=str(listAux[i])
        
        suma=[0,0,0,0,0]
        for i in range(len(self.list_lbl_tabla[0])):
            for j in range(len(self.list_lbl_tabla)):
                suma[i]=float(self.list_lbl_tabla[j][i])+suma[i]
        
        self.crear_labl_tabla()
        
        self.LBLTVTOTCalorias['text']=str(round(suma[0],2))
        self.LBLTVTOTGrasa['text']=str(round(suma[1],2))
        self.LBLTVTOTProteina['text']=str(round(suma[2],2))
        self.LBLTVTOCarb['text']=str(round(suma[3],2))
        self.LBLTVTOFibra['text']=str(round(suma[4],2))
    
    def search_combobox(self,combo_box,event):
        value= event.widget.get()
        if value == '':
            combo_box['values']=self.listacomb
        else:
            data=[]
            for item in self.listacomb:
                if value.lower() in item.lower():
                    data.append(item)
            combo_box['values']= data
    
    def actualizar_label(self,evento):
        # Obtener los valores de los comboboxes
        if (self.EntPORProteina.get()) == '' and (self.EntPORHC.get())== '':
            suma=int(self.EntPORGrasa.get())
        elif (self.EntPORProteina.get()) == '' and (self.EntPORGrasa.get())=='':
            suma= int(self.EntPORHC.get())
        elif (self.EntPORHC.get())== '' and (self.EntPORGrasa.get())=='':
            suma=int(self.EntPORProteina.get())
        elif (self.EntPORProteina.get()) == '':
            suma=int(self.EntPORHC.get())+int(self.EntPORGrasa.get())
        elif (self.EntPORHC.get())== '':
            suma= int(self.EntPORProteina.get())+int(self.EntPORGrasa.get())
        elif (self.EntPORGrasa.get())=='':
            suma= int(self.EntPORProteina.get())+int(self.EntPORHC.get())
        else: suma=int(self.EntPORProteina.get())+int(self.EntPORHC.get())+int(self.EntPORGrasa.get())
            
        # Actualizar el valor del Label
        self.lblPORTOT["text"] = f'Total{suma}'                                                                                      
        # Cambiar el color del Label            
        if suma == 100:                                                                                   
            self.lblPORTOT["bg"] = "green"
            self.lblPORTOT["fg"] = "white"
        else:
            self.lblPORTOT["bg"] = "red"
    
    def actualizar_tres_combobox(self,event):
        opcion_seleccionada = self.combo_Tabla.get()
        self.EntPORProteina.set("")
        self.EntPORHC.set("")
        self.EntPORGrasa.set("")
        self.EntPORProteina["values"]=self.opciones_dependientes2[opcion_seleccionada]["Proteina"]
        self.EntPORHC["values"]=self.opciones_dependientes2[opcion_seleccionada]["HC"]
        self.EntPORGrasa["values"]=self.opciones_dependientes2[opcion_seleccionada]["Grasa"]        
    
    def actualizar_segundo_combobox(self,event):
        opciones_dependientes = {
        "Sedentario": ["1", "1.1"],
        "Ligero": ["1.2", "1.3"],
        "Activo": ["1.4","1.5"],
        "Muy Activo": ["1.6","1.7"],
        "Extremadamente Activo": ["1.8","1.9"],}
        # Obtener la selección del primer combobox
        opcion_seleccionada = self.combo_ActFis.get()
        # Limpiar el segundo combobox
        self.combo_ActFis2.set("")
        # Agregar las opciones correspondientes al segundo combobox
        self.combo_ActFis2["values"] = opciones_dependientes[opcion_seleccionada]
    
    def Calc_GET_Gramos (self):
        self.GETProteina= self.GET2*(int(self.EntPORProteina.get())/100)/4
        self.GETcarbo=self.GET2*(int(self.EntPORHC.get())/100)/4
        self.GETGrasa=self.GET2*(int(self.EntPORGrasa.get())/100)/9

        self.lblGETProteinaGRS['text']= str(round(self.GETProteina,2))+' grs '
        self.lblGETHCGRS['text']= str(round(self.GETcarbo,2))+' grs '
        self.lblGETGrasaGRS['text']= str(round(self.GETGrasa,2))+' grs '
         
    def Calc_GET(self,sexo):
        if sexo =='Femenino':
            TMB=655.09+(9.563*float(self.entryIdentificacion[3].get()))+(1.84*float(self.entryIdentificacion[4].get()))-(4.676*float(self.entryIdentificacion[2].get()))
        else:
            TMB=66.47+(13.75*float(self.entryIdentificacion[3].get()))+(5*float(self.entryIdentificacion[4].get()))-(6.75*float(self.entryIdentificacion[2].get()))

        self.GET=TMB*float(self.combo_ActFis2.get())*1.1
        self.lbl_GET.config(text='Resultado GET: '+str(round(self.GET,2))+' Kcal/dia')

    def Calc_GET2(self,Variable):
        if Variable =='Deficit Calorico':
            self.GET2=self.GET/(1+(float(self.Ent_Valor.get())/100))
        elif Variable =='Normo Calorico':
            self.GET2=self.GET
        else:
            self.GET2=self.GET*(1+(float(self.Ent_Valor.get())/100))
        self.lblGET2.config(text='Requerimiento Calorico: '+ str(round(self.GET2,2))+' Kcal/dia')        
   
    def mostrar_imagen(self,opcion):
        self.imagen_tk = ImageTk.PhotoImage(Image.open(f"images/{opcion}.png").resize((61,161)))
        self.lbl_IMGIMC.config(image=self.imagen_tk)

    def Calc_IMC(self):
        IMC= (float(self.entryIdentificacion[3].get())/(float(self.entryIdentificacion[4].get())/100)**2)
        self.lbl_IMC['text']='Resultado IMC:\n'+ str(round(IMC,2))
        if IMC >= 30:
            self.mostrar_imagen('obesidad')
        elif IMC >=25 and IMC <30:
            self.mostrar_imagen('sobrepeso')
        elif IMC >=18.5 and IMC <25:
            self.mostrar_imagen('normal')
        else:
            self.mostrar_imagen('bajopeso')
        if self.combo_varsexo.get() == 'Femenino':
            self.Calc_GET('Femenino')
        else:
            self.Calc_GET('Masculino')
       
    def Ingresar_Basedatos(self):

        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()

        w=re.findall(r"\d+",self.lbl_IMC.cget('text'))
        x=re.findall(r"\d+",self.lblGET2.cget('text'))
        y=re.findall(r"\d+",self.lblGETProteinaGRS.cget('text'))
        z=re.findall(r"\d+",self.lblGETHCGRS.cget('text'))
        zz=re.findall(r"\d+",self.lblGETGrasaGRS.cget('text'))

        cursor.execute("""
            INSERT INTO PACIENTES (NOMBRE, CEDULA, EDAD,IMC,GET,GETHC,GETPROT,GETGRASA)
            VALUES (?, ?, ?,?,?,?,?,?)
        """,(self.entryIdentificacion[0].get(), self.entryIdentificacion[1].get(), self.entryIdentificacion[2].get(),w[0],x[0],z[0],y[0],zz[0]))
        conexion.commit()
        conexion.close()
        
    def create_menu_window(self):
        MyMenu=tk.Menu(root)
        root.config(menu=MyMenu)
        subMenu1=tk.Menu(MyMenu,tearoff=0)

        MyMenu.add_cascade(label="Archivo", menu=subMenu1)
        subMenu1.add_command(label='Nuevo', command= self.nuevo_paciente)
        subMenu1.add_command(label='Abrir', )
        subMenu1.add_command(label='Guardar', command=self.Ingresar_Basedatos)
        subMenu1.add_separator()
        subMenu1.add_command(label='Salir', command= root.quit)
        subMenu2=tk.Menu(MyMenu,tearoff=0)
        
        MyMenu.add_cascade(label="Opciones", menu=subMenu2)
        subMenu2.add_command(label='Crear Menu',command= self.abrir_ventana1)
        subMenu3=tk.Menu(MyMenu,tearoff=0)
        
        MyMenu.add_cascade(label="Base de Datos", menu=subMenu3)
        subMenu3.add_command(label='Receta Plato',command= self.abrir_ventana4)
        subMenu3.add_command(label='Agregar Alimento',command= self.abrir_ventana2)
        subMenu3.add_command(label='Editar Alimento',command= self.abrir_ventana3)
    
    def Create_widget(self):

        FrameP= tk.Frame(self)
        FrameP.pack()
        Frame=[]
        for i in range (5):
            Frame.append(tk.Frame(FrameP))
            Frame[i].grid(row=i,column=0)
        
        #Primer Frame
        texts=['Nombre:','C.I:','Edad:','Peso (Kg):','Estatura (cm):']
        labelIdentificacion=[]
        self.entryIdentificacion=[]
        for j,i in enumerate(texts):
            labelIdentificacion.append(tk.Label(Frame[0],text=i))
            self.entryIdentificacion.append(tk.Entry(Frame[0],width='10',font=('Arial',10)))
            labelIdentificacion[j].grid(row=0,column=j*2)
            self.entryIdentificacion[j].grid(row=0,column=(j*2)+1)
        self.entryIdentificacion[0].config(width=30)

        self.lbl_sexo= tk.Label (Frame[0],text='Sexo:')   
        self.combo_varsexo=  tk.StringVar()  
        self.combo_sexo = ttk.Combobox(Frame[0], textvariable=self.combo_varsexo, values=['Femenino', 'Masculino'])
               
        self.combo_ActFis=  tk.StringVar() 
        self.combo_ActFis2=  tk.StringVar() 
        self.lbl_ActFis= tk.Label (Frame[0],text='Actividad Fisica:')       
        self.combo_ActFis = ttk.Combobox(Frame[0], textvariable=self.combo_ActFis, values=["Sedentario","Ligero","Activo","Muy Activo","Extremadamente Activo"])
        self.combo_ActFis2 = ttk.Combobox(Frame[0])
        self.combo_ActFis.bind("<<ComboboxSelected>>", self.actualizar_segundo_combobox)
        self.Btn1tn1= tk.Button(Frame[0], text='Aceptar', command=lambda: self.Calc_IMC())
        
        self.combo_sexo.grid(row=1,column=1)
        self.lbl_sexo.grid(row=1,column=0)
        self.lbl_ActFis.grid(row=1,column=2)
        self.combo_ActFis.grid(row=1,column=3)
        self.combo_ActFis2.grid(row=1,column=4)
        self.Btn1tn1.grid(row=3,column=0,columnspan=10)

        #Segundo Frame        
        self.lbl_IMC= tk.Label (Frame[1],text='Resultado IMC:') 
        self.imagen_tk2 = ImageTk.PhotoImage(Image.open("images/normal.png").resize((61,161)))
        self.lbl_IMGIMC= tk.Label(Frame[1], image=self.imagen_tk2)
        self.lbl_GET= tk.Label (Frame[1],text='Resultado GET: 0 Kcal/dia')
        self.lbl_IMC.grid(row=0,column=0)
        self.lbl_IMGIMC.grid(row=0,column=1)        
        self.lbl_GET.grid(row=0,column=2)

        #Tercer Frame
        self.lblGET2=tk.Label(Frame[2],text='Requerimiento Calorico: 0 Kcal/dia')
        self.opciones_dependientes2 = {
        "Deficit Calorico": {
            "Proteina": ["30", "31","32","33","34","35","36","37","38","39","40"],
            "HC": ["30", "31","32","33","34","35","36","37","38","39","40"],
            "Grasa": ["20","21","22","23","24","25","26","27","28","29","30"],
        },
        "Normo Calorico": {
            "Proteina": ["25","26","27","28","29","30"],
            "HC": ["40","41","42","43","44","45","46","47","48","49","50"],
            "Grasa": ["25","26","27","28","29","30"],
        },
        "Superavit Calorico": {
             "Proteina": ["20","21","22","23","24","25"],
            "HC": ["55","56","57","58","59","60"],
            "Grasa": ["20"],
        }, }
        self.combo_vartabla=  tk.StringVar()  
        self.combo_Tabla = ttk.Combobox(Frame[2], textvariable=self.combo_vartabla, values=list(self.opciones_dependientes2.keys()))
        self.Ent_Valor= tk.Entry(Frame[2], width='10',  font=("Arial", 10))
        self.Btn2= tk.Button(Frame[2], text='Aceptar', command= lambda: self.Calc_GET2(self.combo_vartabla.get()))
        self.combo_Tabla.bind("<<ComboboxSelected>>", self.actualizar_tres_combobox)
        self.lblGET2.grid(row=0,column=0) 
        self.combo_Tabla.grid(row=0,column=1)
        self.Ent_Valor.grid(row=0,column=2)
        self.Btn2.grid(row=1,column=0,columnspan=3)

        #Cuarto Frame
        FramePorcentaje=tk.Frame(Frame[3])
        FrameTotGET=tk.Frame(Frame[3])
        FrameBtn3=tk.Frame(Frame[3])
        FramePorcentaje.grid(row=0,column=0)
        FrameTotGET.grid(row=0,column=1)
        FrameBtn3.grid(row=2,column=0,columnspan=2)
        self.lblPORProteina=tk.Label(FramePorcentaje,text= f'% de Proteina')
        self.lblPORHC=tk.Label(FramePorcentaje,text= f'% de HC')
        self.lblPORGrasa=tk.Label(FramePorcentaje,text= f'% de Grasa')
        self.lblPORTOT=tk.Label(FramePorcentaje,text= f'Total %:')
        self.EntPORProteina= ttk.Combobox(FramePorcentaje)
        self.EntPORHC= ttk.Combobox(FramePorcentaje)
        self.EntPORGrasa= ttk.Combobox(FramePorcentaje)

        self.EntPORProteina.bind("<<ComboboxSelected>>", self.actualizar_label)
        self.EntPORHC.bind("<<ComboboxSelected>>", self.actualizar_label)
        self.EntPORGrasa.bind("<<ComboboxSelected>>", self.actualizar_label)

        self.lblPORProteina.grid(row=1,column=0)
        self.lblPORHC.grid(row=0,column=0)
        self.lblPORGrasa.grid(row=2,column=0)
        self.lblPORTOT.grid(row=3,column=1)
        self.EntPORProteina.grid(row=1,column=1)
        self.EntPORHC.grid(row=0,column=1)
        self.EntPORGrasa.grid(row=2,column=1)

        self.lblGETProteina=tk.Label(FrameTotGET,text= 'GET Proteina: ')
        self.lblGETHC=tk.Label(FrameTotGET,text= 'GET Hidratos de Carb: ')
        self.lblGETGrasa=tk.Label(FrameTotGET,text= 'GET Grasa: ')
        self.lblGETProteinaGRS=tk.Label(FrameTotGET,text= '0 gr ')
        self.lblGETHCGRS=tk.Label(FrameTotGET,text= '0 gr ')
        self.lblGETGrasaGRS=tk.Label(FrameTotGET,text= '0 gr ')
        self.lblAUX=tk.Label(FrameTotGET)
        self.Btn3= tk.Button(FrameBtn3, text='Aceptar', command= lambda: self.Calc_GET_Gramos())
       
        self.lblGETProteina.grid(row=1,column=0)
        self.lblGETHC.grid(row=0,column=0)
        self.lblGETGrasa.grid(row=2,column=0)
        self.lblGETProteinaGRS.grid(row=1,column=1)
        self.lblGETHCGRS.grid(row=0,column=1)
        self.lblGETGrasaGRS.grid(row=2,column=1)
        self.lblAUX.grid(row=3,column=1)
        self.Btn3.pack()

        #Quinto Frame
        self.FrameTreeview=tk.Frame(Frame[4])      
        self.FrameTreeview.pack()    
        self.LBLTV= tk.Label(self.FrameTreeview,text='Alimento', background='white', relief='ridge', width=20)

        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT ALIMENTOCOCCION FROM TABLA_NUTRICIONAL")
        self.listacomb = cursor.fetchall()
        conexion.close() 
        self.listacomb = list(map(lambda x: x[0], self.listacomb))
        self.listacomb = [alimento.strip("{}") for alimento in self.listacomb]            
        
        CombTV=[]
        for i in range(9):
            CombTV.append(ttk.Combobox(self.FrameTreeview, values=self.listacomb))
            CombTV[i].grid(row=i+1,column=0)
        
        CombTV[0].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[0], event))
        CombTV[1].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[1], event))
        CombTV[2].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[2], event))
        CombTV[3].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[3], event))
        CombTV[4].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[4], event))
        CombTV[5].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[5], event))
        CombTV[6].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[6], event))
        CombTV[7].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[7], event))
        CombTV[8].bind('<KeyRelease>', lambda event: self.search_combobox(CombTV[8], event))

        
        self.LBLTV2= tk.Label(self.FrameTreeview,text='Consumo (gr)', background='white', relief='ridge', width=20)
        self.LBLTV2.grid(row=0,column=1)
        ENTTV=[]
        for i in range(9):
            ENTTV.append(tk.Entry(self.FrameTreeview, width=24))
            ENTTV[i].grid(row=i+1,column=1)
                
        ENTTV[0].bind("<Return>", lambda event: self.llenar_tabla(CombTV[0],0,event))
        ENTTV[1].bind("<Return>", lambda event: self.llenar_tabla(CombTV[1],1,event))
        ENTTV[2].bind("<Return>", lambda event: self.llenar_tabla(CombTV[2],2,event))
        ENTTV[3].bind("<Return>", lambda event: self.llenar_tabla(CombTV[3],3,event))
        ENTTV[4].bind("<Return>", lambda event: self.llenar_tabla(CombTV[4],4,event))
        ENTTV[5].bind("<Return>", lambda event: self.llenar_tabla(CombTV[5],5,event))
        ENTTV[6].bind("<Return>", lambda event: self.llenar_tabla(CombTV[6],6,event))
        ENTTV[7].bind("<Return>", lambda event: self.llenar_tabla(CombTV[7],7,event))
        ENTTV[8].bind("<Return>", lambda event: self.llenar_tabla(CombTV[8],8,event))

        LBLTV=[]
        textos2=['Calorias (%)','Hidratos de Carb (%)','Proteina (%)','Grasa (%)','Fibra (gr)']
        for j,i in enumerate(textos2):
            LBLTV.append(tk.Label(self.FrameTreeview,text=i, background='white', relief='ridge', width=20))
            LBLTV[j].grid(row=0,column=j+2)
                
        self.list_lbl_tabla=[['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], 
                             ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], 
                             ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0']]
        self.crear_labl_tabla()

        self.LBLTVTOT= tk.Label(self.FrameTreeview,text='TOTAL', background='white', relief='ridge', width=20)
        self.LBLTVTOTCalorias= tk.Label(self.FrameTreeview,text='0', background='white', relief='ridge', width=20)
        self.LBLTVTOTGrasa= tk.Label(self.FrameTreeview,text='0', background='white', relief='ridge', width=20)
        self.LBLTVTOTProteina= tk.Label(self.FrameTreeview,text='0', background='white', relief='ridge', width=20)
        self.LBLTVTOCarb= tk.Label(self.FrameTreeview,text='0', background='white', relief='ridge', width=20)
        self.LBLTVTOFibra= tk.Label(self.FrameTreeview,text='0', background='white', relief='ridge', width=20)

        self.LBLTV.grid(row=0,column=0)     
        self.LBLTVTOT.grid(row=10,column=1)
        self.LBLTVTOTCalorias.grid(row=10,column=2)
        self.LBLTVTOTGrasa.grid(row=10,column=3)
        self.LBLTVTOTProteina.grid(row=10,column=4)
        self.LBLTVTOCarb.grid(row=10,column=5)
        self.LBLTVTOFibra.grid(row=10,column=6)

        conexion = sqlite3.connect("mibasedatos.db")
        cursor = conexion.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS PACIENTES (
            CODIGO INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE TEXT,
            CEDULA TEXT,
            EDAD TEXT,
            IMC TEXT,
            GET TEXT,
            GETHC TEXT,
            GETPROT TEXT ,
            GETGRASA TEXT                                        
        )
        """)
        conexion.commit()
        conexion.close()


if __name__ == "__main__":
    root = tk.Tk()
    mywindow(root).pack(side="top", fill="both", expand=True)
    root.title('Nutricion Celular')
    root.mainloop()