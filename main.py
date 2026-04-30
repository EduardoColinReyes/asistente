import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import voz as tav
from ia import *
from pynput import keyboard
import webbrowser, os
from tkinter import filedialog


def guardar_historial():
    contenido_historial = txahistorial.get("1.0", tk.END)    
    if contenido_historial.strip() == "":
        messagebox.showwarning("Advertencia", "No hay historial para guardar.")
        return

    archivo = filedialog.asksaveasfilename(
        initialfile="historial_asistente.txt",
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )

    if archivo:
        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(contenido_historial)
            messagebox.showinfo("Éxito", "Historial guardado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")


def abrir_url(url):
    webbrowser.open(url)

# Funcion para cambiar tamaño de la imagen
def cambiar_imagen(ubicacion, tamaño):
    return ImageTk.PhotoImage(Image.open(ubicacion).resize(tamaño))

def conversacion():
    texto_usuario = txtprompt.get().strip()    
    if texto_usuario == "":
        txahistorial.insert(tk.INSERT, "No entiendo, ¿podrías ser más específico?\n")
        tav.hablar("No entiendo, podrías ser más específico.")
    else:
        lista = texto_usuario.lower().split()
        print(lista)

        for busqueda in lista:
            if busqueda in respuestas:
                txahistorial.insert(tk.INSERT, f"Usuario: {texto_usuario.lower()}\nAsistente: Aquí tienes {respuestas[busqueda]}\n") 
                tav.hablar(respuestas[busqueda])
                txtprompt.delete(0, tk.END)
                txtprompt.focus()
                return 

            if busqueda in webs:
                txahistorial.insert(tk.INSERT, f"Usuario: {texto_usuario.lower()}\nAsistente: Abriendo {busqueda}\n") 
                tav.hablar("Aquí tienes " + busqueda)
                abrir_url(webs[busqueda])
                txtprompt.delete(0, tk.END)
                txtprompt.focus()
                return

        # Si no encontró nada en respuestas ni en webs
        resultado = "https://www.google.com/search?q=" + texto_usuario.lower()
        txahistorial.insert(tk.INSERT, f"Usuario: {texto_usuario.lower()}\nAsistente: No tengo conocimiento sobre lo que buscabas, pero encontré esto en la web para ti.\n") 
        tav.hablar("No tengo conocimiento sobre lo que buscabas, pero encontré esto en la web para ti.")
        abrir_url(resultado)
        txtprompt.delete(0, tk.END)
        txtprompt.focus()

def detectar_enter(key):
    if key == keyboard.Key.enter:
        conversacion()

#Iniciar el listener del teclado
listener = keyboard.Listener(on_press=detectar_enter)
listener.start()

#Creacion de la ventana principal
interfaz = tk.Tk()
interfaz.title("Asistente")
interfaz.geometry("650x650")
interfaz.resizable(False, False)

#Crear marco para el encabezado
encabezado = tk.Frame(interfaz, height=70, bg="#000000", relief=tk.SOLID)
encabezado.pack(side="top", fill="x")

#Texto del encabeado
lbltitulo_encabezado = tk.Label(encabezado, text="¡¡¡ Bienvenidos !!!",
                     font=("Nunito", 22, "bold"),
                     bg="#000000",
                     pady=25,
                     fg="#f8f9fa"
                     )
lbltitulo_encabezado.pack(fill="both", expand=True)

#Seccion que tendra todo el contenido
contenido = tk.Frame(interfaz, bg="#ffffff", padx=10, pady=10)
contenido.pack(side="bottom", fill="both", expand=True)

#Añadir la imagen
imgasistente = cambiar_imagen("asistente.png", (130, 130))
lblimagen = tk.Label(contenido, image=imgasistente, bg="#ffffff")
lblimagen.grid(row=0, column=0, columnspan=2)

lblinstruccion = tk.Label(contenido,
                     text="Iniciar conversación con el asistente",
                     font=("Nunito", 14), 
                     pady=10,
                     bg="#ffffff",
                     fg="#212529"
                     )
lblinstruccion.grid(row=1, column=0, columnspan=2)

#Recibimiento de los datos recibidos por el usuario
txtprompt = tk.Entry(contenido, width=40, font=("Nunito", 14),
                     bg="#e5e5e5",
                     highlightbackground="black",
                     highlightthickness=1
                     )
txtprompt.grid(row=2, column=0, columnspan=2)

#Para que se muestre la conversacion
txahistorial = tk.Text(contenido, font=("Nunito", 8),
                       height=15, width=100,
                       highlightbackground="#000000",
                       highlightthickness=1,
                       bg="#e5e5e5"
                       )
txahistorial.grid(row=3, column=0, pady=10, columnspan=2)

#Botones
btnenviar = tk.Button(contenido, text="Enviar mensaje", 
                      font=("Nunito", 14, "bold"),
                      height=2, width=20, 
                      fg="#ffffff",
                      bg="#14213d",
                      command=conversacion
                      )
btnenviar.grid(row=4, column=0)

btnguardar = tk.Button(contenido, text="Guardar", 
                      font=("Nunito", 14, "bold"),
                      height=2, width=20, 
                      fg="#ffffff",
                      bg="#14213d",
                      command=guardar_historial 
                      )
btnguardar.grid(row=4, column=1)

txtprompt.focus()

interfaz.mainloop()