from tkinter import Tk, Label, Button, Entry,filedialog,Frame

def DirArch():
    ruta = filedialog.askopenfilename()
    Ent.delete(0, 'end')
    Ent.insert(0, ruta)


window = Tk()
window.geometry('400x400')
window.title('Mensajeria Masiva')

frame1= Frame(window, bg='green')
frame2= Frame(window, bg='green')
frame3= Frame(window, bg='green')
frame4= Frame(window, bg='green')

frame1.pack(expand=True,fill='both')
frame2.pack(expand=True,fill='both')
frame3.pack(expand=True,fill='both')
frame4.pack(expand=True,fill='both')

lbl= Label (frame1,text='Ubicacion de Archivo de Excel:')
btn= Button(frame1, text='Examinar',  command=DirArch)
Ent= Entry(frame1)
lbl2= Label (frame2, text='Mensaje a Enviar')
Ent2= Entry(frame3)
btn2= Button(frame4, text='Aceptar')

lbl.place(relx=.05,rely=.05,relwidth=.25,relheight=.2)
btn.place(relx=.65,rely=.05,relwidth=.25,relheight=.2)
Ent.place(relx=.35,rely=.05,relwidth=.25,relheight=.2)
lbl2.place(relx=.5,rely=.5)
Ent2.pack()
btn2.pack()


window.mainloop()
