import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, controlador):
        self.controlador = controlador

        self.root = tk.Tk()
        self.root.title("Acceso a linea de produccion")
        self.root.geometry("350x250")
        self.root.config(bg="#222")

        tk.Label(self.root, text="Usuario", fg ="white", bg ="#222").pack()
        self.usuario=tk.Entry(self.root)
        self.usuario.pack()

        tk.Label(self.root, text="Contraseña:", fg="white", bg="#222").pack()
        self.password = tk.Entry(self.root, show ="*")
        self.password.pack()

        tk.Button(
            self.root,
            text="ingresar",
            command=self.login,
            bg="#00A884",
            fg="white",
            width=20
            ).pack()
        
        self.root.mainloop()

    def login(self):
        error = self.controlador.login(
            self.usuario.get(),
            self.password.get(),
            self.root
        )

        if error:
            messagebox.showerror("Error", error)