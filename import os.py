import os
import shutil
import tkinter as tk
from tkinter import filedialog

class MyApp:
    def __init__(self, master):
        self.master = master
        master.title("organizador de archivos")

        self.textbox = tk.Entry(master, width=50)
        self.textbox.pack()

        self.seleccionar_carpeta = tk.Button(master, text="Seleccionar carpeta", command=self.abrir_dialogo_carpeta)
        self.seleccionar_carpeta.pack()

        self.ejecutar_programa = tk.Button(master, text="Ejecutar programa", command=self.ejecutar)
        self.ejecutar_programa.pack()

        self.label = tk.Label(master, text="")
        self.label.pack()

    def abrir_dialogo_carpeta(self):
        carpeta_seleccionada = filedialog.askdirectory()
        self.textbox.delete(0, tk.END)
        self.textbox.insert(0, carpeta_seleccionada)

    def ejecutar(self):
        #es la carpeta que se va a organizar
        carpeta_destino = self.textbox.get()
        #es el programa guardado
        programa_origen = "C:\\Users\\usuario\\Documents\\root\\python\\directoryo\\prom\\organizador\\org_file\\org_file.py"
        programa_destino = os.path.join(carpeta_destino, programa_origen)
        print(f"ruta del archivo {programa_destino}")
        shutil.copy(programa_destino,carpeta_destino)
        os.chdir(carpeta_destino)
        os.system("python org_file.py")
        try:
            if os.path.exists(carpeta_destino):
                os.remove("PROGRAMAN\\org_file.py")
                os.remove("org_file.py")
                os.remove("OTHERS\\org_file.py")
                
                
                print(f"el archivo fue eliminado existosamente.")
            else:
                print(f"el archivo {programa_destino} no existe.")
        except WindowsError:
            print('encotrado archivo')
        self.label.configure(text=f"Programa ejecutado en: {carpeta_destino}")

root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
