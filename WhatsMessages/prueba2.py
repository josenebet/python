import tkinter as tk
from PIL import Image, ImageTk

# Lista de emojis de WhatsApp
emojis = [
    "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "☀️", "", "", "", "",
    "", "", "", "", "", "", "", "", "⭐️", "",
    "", "☁️", "⛅️", "⛈", "", "", "❄️", "☃️", "⛄️", "",
    "", "", "", "☔️", "☂️", "", "", "", "", "⛰",
    "", "", , "", "", "", "", "", "", "",
    "", ", "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "⛪️", "", "",
    "⛩", "", "", "", "", "", "", "", "", "",
    "", "", "🪃", "🪪", "🪫", "🪬", "🪽", "🪾", "🪿",
    "🪢", "🪃", "🪪", "🪫", "🪬", "🪽", "🪾", "🪿", "🪢",
]

class EmojiApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        # Crear el objeto Text
        self.text = tk.Text(self, height=10, width=50)
        self.text.pack()

        # Crear el scrollbar
        self.scrollbar = tk.Scrollbar(self, command=self.text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.config(yscrollcommand=self.scrollbar.set)

        # Crear el frame para los botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack()

        # Crear los botones
        for emoji in emojis:
            boton = tk.Button(self.frame_botones, text=emoji, command=lambda emoji=emoji: self.insertar_emoji(emoji))
            boton.pack(side=tk.LEFT)

    def insertar_emoji(self, emoji):
        # Insertar el emoji en el objeto Text
        self.text.insert("insert", emoji)

# Crear la ventana principal
root = tk.Tk()
root.title("Emojis de WhatsApp")

# Crear la aplicación
app = EmojiApp(root)
app.pack()

# Iniciar el bucle principal
root.mainloop()
