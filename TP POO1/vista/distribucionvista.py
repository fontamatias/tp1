import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

class DistribucionVista:
    def __init__(self, controlador, usuario):
        self.controlador = controlador
        self.usuario = usuario

        self.root = tk.Tk()
        self.root.title("Distribución / Ventas")

        hoy = date.today().isoformat()
        tk.Label(self.root, text=f"Fecha: {hoy}", font=("Arial", 12, "bold")).pack()
        tk.Label(self.root, text=f"Usuario: {usuario}", font=("Arial", 12, "bold")).pack()

        # Stock
        tk.Label(self.root, text="Stock de motos (Moto, Motor)").pack()
        self.tree_stock = ttk.Treeview(self.root, columns=("moto","motor"), show="headings", height=6)
        self.tree_stock.heading("moto", text="Moto")
        self.tree_stock.heading("motor", text="Motor")
        self.tree_stock.pack()

        # Formulario de venta
        form = tk.Frame(self.root)
        form.pack(pady=8)
        tk.Label(form, text="Número moto:").grid(row=0, column=0, sticky="e")
        self.num_moto = tk.Entry(form)
        self.num_moto.grid(row=0, column=1)

        tk.Label(form, text="Número chasis:").grid(row=1, column=0, sticky="e")
        self.num_chasis = tk.Entry(form)
        self.num_chasis.grid(row=1, column=1)

        tk.Label(form, text="Cantidad:").grid(row=2, column=0, sticky="e")
        self.cantidad = tk.Entry(form)
        self.cantidad.insert(0,"1")
        self.cantidad.grid(row=2, column=1)

        tk.Label(form, text="Comprador:").grid(row=3, column=0, sticky="e")
        self.comprador = tk.Entry(form)
        self.comprador.grid(row=3, column=1)

        tk.Label(form, text="Dársena:").grid(row=4, column=0, sticky="e")
        self.darsena = tk.Entry(form)
        self.darsena.grid(row=4, column=1)

        tk.Button(self.root, text="Generar pedido / Vender", bg="#00A884", fg="white", command=self.vender).pack(pady=6)
        tk.Button(self.root, text="Actualizar stock", command=self.actualizar_stock).pack()

        # Ventana de ventas realizadas
        tk.Label(self.root, text="Pedidos / Ventas registradas").pack(pady=(10,0))
        self.tree_ventas = ttk.Treeview(self.root, columns=("pedido","moto","chasis","cant","comprador","darsena","fecha"), show="headings", height=6)
        for col, txt in [("pedido","Pedido"),("moto","Moto"),("chasis","Chasis"),("cant","Cant"),("comprador","Comprador"),("darsena","Darsena"),("fecha","Fecha")]:
            self.tree_ventas.heading(col, text=txt)
        self.tree_ventas.pack()

        self.actualizar_stock()
        self.actualizar_ventas()
        self.root.mainloop()

    def actualizar_stock(self):
        for i in self.tree_stock.get_children():
            self.tree_stock.delete(i)
        for m in self.controlador.listar_stock():
            self.tree_stock.insert("", tk.END, values=m)

    def actualizar_ventas(self):
        for i in self.tree_ventas.get_children():
            self.tree_ventas.delete(i)
        for v in self.controlador.listar_ventas():
            # v: (id, pedido_num, num_moto, num_chasis, cantidad, comprador, darsena, fecha)
            self.tree_ventas.insert("", tk.END, values=(v[1], v[2], v[3], v[4], v[5], v[6], v[7]))

    def vender(self):
        num_moto = self.num_moto.get()
        num_chasis = self.num_chasis.get()
        cantidad = self.cantidad.get()
        comprador = self.comprador.get()
        darsena = self.darsena.get()

        ok, info = self.controlador.crear_pedido(num_moto, num_chasis, cantidad, comprador, darsena)
        if ok:
            messagebox.showinfo("Pedido generado", f"Pedido: {info}")
            self.actualizar_stock()
            self.actualizar_ventas()
        else:
            messagebox.showerror("Error", info)