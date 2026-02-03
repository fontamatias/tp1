import tkinter as tk
from tkinter import ttk
from datetime import date

class Sistema:
    def __init__(self, controlador, operario):
        self.controlador = controlador
        self.operario = operario

        self.root = tk.Tk()
        self.root.title("Linea de produccion")

        hoy = date.today().isoformat()
        tk.Label(
            self.root,
            text=f"Fecha de hoy es : {hoy}",
            font=("Arial", 12, "bold")
        ).pack()

        tk.Label(
            self.root,
            text=f"Operario: {operario}",
            font=("Arial", 12, "bold")
        ).pack()

        # ===== ENTRADAS =====
        tk.Label(self.root, text="Numero de moto:").pack()
        self.numero_moto = tk.Entry(self.root, bg="#9F24E3", fg="white")
        self.numero_moto.pack()

        tk.Label(self.root, text="Numero de motor:").pack()
        self.n_motor = tk.Entry(self.root, bg="#9F24E3", fg="white")
        self.n_motor.pack()

        tk.Label(self.root, text="Defecto (1-3):").pack()
        self.defecto = tk.Entry(self.root, bg="#9F24E3", fg="white")
        self.defecto.pack()

        tk.Button(
            self.root,
            text="ALTA (OK)",
            bg="#00FA95",
            fg="white",
            command=self.alta
        ).pack()

        tk.Button(
            self.root,
            text="BAJA (NO OK)",
            bg="#FA1A00",
            fg="white",
            command=self.baja
        ).pack()

        # ===== CONSULTA =====
        tk.Label(
            self.root,
            text="Numero de moto para buscar o modificar"
        ).pack()

        self.consulta = tk.Entry(self.root)
        self.consulta.pack()

        tk.Button(
            self.root,
            text="Mover de mecanica a OK",
            command=self.mover
        ).pack()

        tk.Button(
            self.root,
            text="Buscar estado de moto",
            command=self.buscar
        ).pack()

        tk.Button(
            self.root,
            text="Terminar el día",
            command=self.final_dia
        ).pack(pady=15)

        self.salida = tk.Label(self.root, text="", font=("Arial", 12))
        self.salida.pack()

        # ===== LISTAS =====
        contenedor = tk.Frame(self.root)
        contenedor.pack()

        tk.Label(contenedor, text="Motos OK").grid(row=0, column=0)
        self.lista_ok = ttk.Treeview(
            contenedor,
            columns=("moto", "motor"),
            show="headings",
            height=6
        )
        self.lista_ok.heading("moto", text="Moto")
        self.lista_ok.heading("motor", text="Motor")
        self.lista_ok.grid(row=1, column=0)

        tk.Label(contenedor, text="Motos NO OK").grid(row=0, column=1)
        self.lista_no_ok = ttk.Treeview(
            contenedor,
            columns=("moto", "motor", "defecto"),
            show="headings",
            height=6
        )
        self.lista_no_ok.heading("moto", text="Moto")
        self.lista_no_ok.heading("motor", text="Motor")
        self.lista_no_ok.heading("defecto", text="Defecto")
        self.lista_no_ok.grid(row=1, column=1)

        # Botón sorpresa
        tk.Button(
            self.root,
            text="Sorpresa",
            command=self.cambiar_color
        ).pack(side="left", anchor="s", padx=10, pady=10)

        self.actualizar_listas()
        self.root.mainloop()

    def actualizar_listas(self):
        self.lista_ok.delete(*self.lista_ok.get_children())
        self.lista_no_ok.delete(*self.lista_no_ok.get_children())

        for m in self.controlador.listar_ok():
            self.lista_ok.insert("", tk.END, values=m)

        for m in self.controlador.listar_no_ok():
            self.lista_no_ok.insert("", tk.END, values=m)

    def alta(self):
        ok = self.controlador.alta(
            self.numero_moto.get(),
            self.n_motor.get(),
        )
        self.salida.config(
            text="Moto cargada como OK" if ok else "Error en los datos"
        )
        self.actualizar_listas()

    def baja(self):
        ok = self.controlador.baja(
            self.numero_moto.get(),
            self.n_motor.get(),
            self.defecto.get()
        )
        self.salida.config(
            text="Moto enviada a mecánica" if ok else "Defecto inválido"
        )
        self.actualizar_listas()

    def mover(self):
        ok = self.controlador.mover_a_ok(self.consulta.get())
        self.salida.config(
            text="Moto movida a OK" if ok else "Moto no encontrada"
        )
        self.actualizar_listas()

    def buscar(self):
        res = self.controlador.buscar(self.consulta.get())
        self.salida.config(text=res)

    def final_dia(self):
        ok, no_ok = self.controlador.resumen()
        self.salida.config(
            text=f"Motos OK: {ok} -- Motos NO OK: {no_ok}"
        )

    def cambiar_color(self):
        self.controlador.cambiar_color(self.root)
