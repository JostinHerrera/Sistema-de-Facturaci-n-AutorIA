import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class SistemaAutorIA:
    def __init__(self, root):
        self.root = root
        self.root.title("AutorIA - Sistema de Gestión de Facturación e Inventario")
        self.root.geometry("900x650")

        self.archivo_datos = "datos_autor_ia.json"
        self.cargar_datos()

        # Configuración de estilos
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # Creación de pestañas (Notebook)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Pestaña 1: Facturación
        self.tab_facturacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_facturacion, text="Generar Factura")
        self.configurar_pestaña_facturacion()

        # Pestaña 2: Gestión de Inventario
        self.tab_inventario = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_inventario, text="Gestión de Inventario")
        self.configurar_pestaña_inventario()

        # Pestaña 3: Historial
        self.tab_historial = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_historial, text="Historial de Ventas")
        self.configurar_pestaña_historial()

        # Pestaña 4: Movimientos
        self.tab_movimientos = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_movimientos, text="Movimientos de Inventario")
        self.configurar_pestaña_movimientos()

    def registrar_movimiento(self, id_item, nombre, tipo, cantidad, stock_prev, stock_nuevo, precio_unit):
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        monto = abs(cantidad * precio_unit)

        # Lógica contable básica:
        # Si entra stock (cantidad > 0) o es alta: DEBE (Inversión/Entrada)
        # Si sale stock (cantidad < 0): HABER (Salida/Venta)
        monto_debe = monto if cantidad > 0 else 0
        monto_haber = monto if cantidad < 0 else 0

        self.movimientos.append({
            "fecha": fecha,
            "id": id_item,
            "nombre": nombre,
            "tipo": tipo,
            "cantidad": cantidad,
            "prev": stock_prev,
            "nuevo": stock_nuevo,
            "monto_debe": monto_debe,
            "monto_haber": monto_haber
        })
        self.actualizar_tabla_movimientos()

    def cargar_datos(self):
        """Carga el inventario y el historial desde un archivo JSON o usa valores por defecto."""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.inventario = datos.get("inventario", {})
                    self.historial = datos.get("historial", [])
                    self.movimientos = datos.get("movimientos", [])
            except Exception as e:
                print(f"Error al cargar datos: {e}")
                self.inicializar_predeterminado()
        else:
            self.inicializar_predeterminado()

    def inicializar_predeterminado(self):
        self.inventario = {
            "1": ["Chatbot Básico", 500.0, 10],
            "2": ["Automatización de Emails", 300.0, 15],
            "3": ["Consultoría IA", 150.0, 5]
        }
        self.historial = []
        self.movimientos = []
        self.guardar_datos()

    def guardar_datos(self):
        """Guarda el estado actual en el archivo JSON."""
        datos = {
            "inventario": self.inventario,
            "historial": self.historial,
            "movimientos": self.movimientos
        }
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los datos: {e}")

    # --- PESTAÑA: FACTURACIÓN ---
    def configurar_pestaña_facturacion(self):
        # Frame superior: Datos del cliente
        frame_cliente = ttk.LabelFrame(self.tab_facturacion, text="Datos del Cliente", padding=10)
        frame_cliente.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_cliente, text="Nombre/Empresa:").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_cliente = ttk.Entry(frame_cliente, width=40)
        self.entry_cliente.grid(row=0, column=1, sticky="w", padx=5)

        # Frame medio: Selección de servicios
        frame_seleccion = ttk.LabelFrame(self.tab_facturacion, text="Selección de Servicios", padding=10)
        frame_seleccion.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_seleccion, text="Servicio:").grid(row=0, column=0, sticky="w", padx=5)
        self.combo_servicios = ttk.Combobox(frame_seleccion, state="readonly", width=40)
        self.combo_servicios.grid(row=0, column=1, sticky="w", padx=5)
        self.actualizar_combo_servicios()

        ttk.Label(frame_seleccion, text="Cantidad:").grid(row=0, column=2, sticky="w", padx=5)
        self.spin_cantidad = ttk.Spinbox(frame_seleccion, from_=1, to=100, width=5)
        self.spin_cantidad.set(1)
        self.spin_cantidad.grid(row=0, column=3, sticky="w", padx=5)

        btn_agregar = ttk.Button(frame_seleccion, text="Agregar a Lista", command=self.agregar_a_factura)
        btn_agregar.grid(row=0, column=4, padx=10)

        # Tabla de items de la factura actual
        self.tree_factura = ttk.Treeview(self.tab_facturacion, columns=("id", "nombre", "precio", "cantidad", "subtotal"), show="headings", height=8)
        self.tree_factura.heading("id", text="ID")
        self.tree_factura.heading("nombre", text="Servicio")
        self.tree_factura.heading("precio", text="Precio Unit.")
        self.tree_factura.heading("cantidad", text="Cant.")
        self.tree_factura.heading("subtotal", text="Subtotal")

        self.tree_factura.column("id", width=50)
        self.tree_factura.column("nombre", width=250)
        self.tree_factura.column("precio", width=100)
        self.tree_factura.column("cantidad", width=80)
        self.tree_factura.column("subtotal", width=100)
        self.tree_factura.pack(fill="both", expand=True, padx=10, pady=5)

        # Frame inferior: Totales y Acciones
        frame_totales = ttk.Frame(self.tab_facturacion)
        frame_totales.pack(fill="x", padx=10, pady=10)

        self.lbl_total_var = tk.StringVar(value="Total: $0.00")
        lbl_total = ttk.Label(frame_totales, textvariable=self.lbl_total_var, font=('Helvetica', 12, 'bold'))
        lbl_total.pack(side="right", padx=10)

        btn_limpiar = ttk.Button(frame_totales, text="Limpiar Todo", command=self.limpiar_factura)
        btn_limpiar.pack(side="left", padx=5)

        btn_finalizar = ttk.Button(frame_totales, text="Finalizar y Cobrar", command=self.finalizar_factura)
        btn_finalizar.pack(side="left", padx=5)

        self.items_factura_actual = []

    def actualizar_combo_servicios(self):
        lista = [f"{id} - {datos[0]} (${datos[1]})" for id, datos in self.inventario.items()]
        self.combo_servicios['values'] = lista
        if lista:
            self.combo_servicios.current(0)

    def agregar_a_factura(self):
        seleccion = self.combo_servicios.get()
        if not seleccion: return

        id_item = seleccion.split(" - ")[0]
        cantidad = int(self.spin_cantidad.get())

        nombre, precio, stock = self.inventario[id_item]

        # Verificar stock
        # Contar ya agregados en la lista actual
        cant_ya_agregada = sum(item['cantidad'] for item in self.items_factura_actual if item['id'] == id_item)

        if (cant_ya_agregada + cantidad) > stock:
            messagebox.showwarning("Sin Stock", f"No hay suficiente stock para {nombre}. Disponible: {stock}")
            return

        subtotal = precio * cantidad
        self.items_factura_actual.append({
            'id': id_item,
            'nombre': nombre,
            'precio': precio,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

        self.tree_factura.insert("", "end", values=(id_item, nombre, f"${precio:.2f}", cantidad, f"${subtotal:.2f}"))
        self.actualizar_total_factura()

    def actualizar_total_factura(self):
        total = sum(item['subtotal'] for item in self.items_factura_actual)
        total_con_iva = total * 1.15
        self.lbl_total_var.set(f"Total (IVA 15%): ${total_con_iva:.2f}")

    def limpiar_factura(self):
        for item in self.tree_factura.get_children():
            self.tree_factura.delete(item)
        self.items_factura_actual = []
        self.entry_cliente.delete(0, tk.END)
        self.actualizar_total_factura()

    def finalizar_factura(self):
        cliente = self.entry_cliente.get().strip()
        if not cliente:
            messagebox.showerror("Error", "Debe ingresar el nombre del cliente.")
            return
        if not self.items_factura_actual:
            messagebox.showerror("Error", "La factura está vacía.")
            return

        # Confirmar y actualizar inventario
        total_venta = sum(item['subtotal'] for item in self.items_factura_actual) * 1.15
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Registro para historial
        venta = {
            "fecha": fecha,
            "cliente": cliente,
            "items": self.items_factura_actual.copy(),
            "total": total_venta
        }

        # Descontar stock de verdad y registrar movimientos
        for item in self.items_factura_actual:
            stock_anterior = self.inventario[item['id']][2]
            nuevo_stock = stock_anterior - item['cantidad']
            self.inventario[item['id']][2] = nuevo_stock

            self.registrar_movimiento(
                item['id'],
                item['nombre'],
                "SALIDA (Venta)",
                -item['cantidad'],
                stock_anterior,
                nuevo_stock,
                item['precio']
            )

        self.historial.append(venta)
        self.guardar_datos()
        self.actualizar_tabla_inventario() # Actualizar vista de inventario
        self.actualizar_tabla_historial() # Actualizar vista de historial
        self.actualizar_combo_servicios() # Por si cambió disponibilidad drásticamente

        # Mostrar resumen tipo factura
        mensaje_factura = f"FACTURA: AutorIA\nFECHA: {fecha}\nCLIENTE: {cliente}\n" + "="*30 + "\n"
        for item in self.items_factura_actual:
            mensaje_factura += f"{item['nombre']} x{item['cantidad']}: ${item['subtotal']:.2f}\n"
        mensaje_factura += "="*30 + f"\nTOTAL (IVA Inc.): ${total_venta:.2f}"

        messagebox.showinfo("Venta Exitosa", mensaje_factura)
        self.limpiar_factura()

    # --- PESTAÑA: INVENTARIO ---
    def configurar_pestaña_inventario(self):
        # Frame para el formulario de edición/creación
        frame_form = ttk.LabelFrame(self.tab_inventario, text="Producto / Servicio", padding=10)
        frame_form.pack(side="top", fill="x", padx=10, pady=10)

        ttk.Label(frame_form, text="ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_inv_id = ttk.Entry(frame_form, width=10)
        self.entry_inv_id.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_inv_nombre = ttk.Entry(frame_form, width=30)
        self.entry_inv_nombre.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Precio:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_inv_precio = ttk.Entry(frame_form, width=10)
        self.entry_inv_precio.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Stock:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.entry_inv_stock = ttk.Entry(frame_form, width=10)
        self.entry_inv_stock.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        # Botones de acción para inventario
        frame_btns_inv = ttk.Frame(frame_form)
        frame_btns_inv.grid(row=2, column=0, columnspan=4, pady=10)

        ttk.Button(frame_btns_inv, text="Guardar / Actualizar", command=self.guardar_producto_inventario).pack(side="left", padx=5)
        ttk.Button(frame_btns_inv, text="Eliminar Seleccionado", command=self.eliminar_producto_inventario).pack(side="left", padx=5)
        ttk.Button(frame_btns_inv, text="Limpiar Formulario", command=self.limpiar_form_inventario).pack(side="left", padx=5)

        # Resumen de Valor de Inventario
        self.lbl_valor_inv_var = tk.StringVar(value="Valor Total del Inventario: $0.00")
        lbl_valor_inv = ttk.Label(self.tab_inventario, textvariable=self.lbl_valor_inv_var, font=('Helvetica', 10, 'bold'), foreground="blue")
        lbl_valor_inv.pack(pady=5)

        # Tabla de inventario
        self.tree_inventario = ttk.Treeview(self.tab_inventario, columns=("id", "nombre", "precio", "stock", "valor_total"), show="headings")
        self.tree_inventario.heading("id", text="ID")
        self.tree_inventario.heading("nombre", text="Servicio / Producto")
        self.tree_inventario.heading("precio", text="Precio Unitario")
        self.tree_inventario.heading("stock", text="Stock")
        self.tree_inventario.heading("valor_total", text="Valor Total")

        self.tree_inventario.column("id", width=60)
        self.tree_inventario.column("nombre", width=250)
        self.tree_inventario.column("precio", width=100)
        self.tree_inventario.column("stock", width=80)
        self.tree_inventario.column("valor_total", width=120)
        self.tree_inventario.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_inventario.bind("<<TreeviewSelect>>", self.cargar_producto_seleccionado)
        self.actualizar_tabla_inventario()

    def actualizar_tabla_inventario(self):
        for item in self.tree_inventario.get_children():
            self.tree_inventario.delete(item)

        valor_acumulado = 0
        for id_item, datos in sorted(self.inventario.items()):
            nombre, precio, stock = datos
            total_producto = precio * stock
            valor_acumulado += total_producto
            self.tree_inventario.insert("", "end", values=(id_item, nombre, f"${precio:.2f}", stock, f"${total_producto:.2f}"))

        self.lbl_valor_inv_var.set(f"Valor Total del Inventario (Capital en Stock): ${valor_acumulado:.2f}")
        self.actualizar_combo_servicios()

    def cargar_producto_seleccionado(self, event):
        seleccion = self.tree_inventario.selection()
        if not seleccion: return

        item_data = self.tree_inventario.item(seleccion[0], 'values')
        self.limpiar_form_inventario()
        self.entry_inv_id.insert(0, item_data[0])
        self.entry_inv_nombre.insert(0, item_data[1])
        self.entry_inv_precio.insert(0, item_data[2].replace('$', ''))
        self.entry_inv_stock.insert(0, item_data[3])
        # Bloquear edición de ID si se va a actualizar? No, pero suele ser mejor así.

    def limpiar_form_inventario(self):
        self.entry_inv_id.delete(0, tk.END)
        self.entry_inv_nombre.delete(0, tk.END)
        self.entry_inv_precio.delete(0, tk.END)
        self.entry_inv_stock.delete(0, tk.END)

    def guardar_producto_inventario(self):
        idx = self.entry_inv_id.get().strip()
        nombre = self.entry_inv_nombre.get().strip()
        try:
            precio = float(self.entry_inv_precio.get().strip())
            stock = int(self.entry_inv_stock.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Precio y Stock deben ser números válidos.")
            return

        if not idx or not nombre:
            messagebox.showerror("Error", "ID y Nombre son obligatorios.")
            return

        # Registrar si es un ajuste de stock o entrada
        tipo_mov = "AJUSTE"
        stock_anterior = 0
        if idx in self.inventario:
            stock_anterior = self.inventario[idx][2]
            diferencia = stock - stock_anterior
            if diferencia > 0: tipo_mov = "ENTRADA"
            elif diferencia < 0: tipo_mov = "AJUSTE/SALIDA"
            cant_mov = diferencia
        else:
            tipo_mov = "ALTA INICIAL"
            cant_mov = stock

        if cant_mov != 0 or tipo_mov == "ALTA INICIAL":
            self.registrar_movimiento(idx, nombre, tipo_mov, cant_mov, stock_anterior, stock, precio)

        self.inventario[idx] = [nombre, precio, stock]
        self.guardar_datos()
        self.actualizar_tabla_inventario()
        self.limpiar_form_inventario()
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")

    def eliminar_producto_inventario(self):
        seleccion = self.tree_inventario.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un producto de la tabla.")
            return

        item_data = self.tree_inventario.item(seleccion[0], 'values')
        idx = item_data[0]

        if messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar '{item_data[1]}'?"):
            if idx in self.inventario:
                precio_unit = self.inventario[idx][1]
                self.registrar_movimiento(idx, item_data[1], "ELIMINACIÓN", -int(item_data[3]), int(item_data[3]), 0, precio_unit)
                del self.inventario[idx]
                self.guardar_datos()
                self.actualizar_tabla_inventario()
                self.limpiar_form_inventario()

    # --- PESTAÑA: HISTORIAL ---
    def configurar_pestaña_historial(self):
        # Instrucciones
        ttk.Label(self.tab_historial, text="Doble clic en una venta para ver el detalle de productos", font=('Helvetica', 9, 'italic')).pack(pady=5)

        self.tree_historial = ttk.Treeview(self.tab_historial, columns=("fecha", "cliente", "total"), show="headings")
        self.tree_historial.heading("fecha", text="Fecha y Hora")
        self.tree_historial.heading("cliente", text="Cliente")
        self.tree_historial.heading("total", text="Total Facturado")

        self.tree_historial.column("fecha", width=180)
        self.tree_historial.column("cliente", width=250)
        self.tree_historial.column("total", width=120)

        scroll = ttk.Scrollbar(self.tab_historial, orient="vertical", command=self.tree_historial.yview)
        self.tree_historial.configure(yscrollcommand=scroll.set)

        self.tree_historial.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scroll.pack(side="right", fill="y", pady=10, padx=(0,10))

        self.tree_historial.bind("<Double-1>", self.ver_detalle_factura)
        self.actualizar_tabla_historial()

    def ver_detalle_factura(self, event):
        seleccion = self.tree_historial.selection()
        if not seleccion: return

        # Obtener el índice de la venta seleccionada (considerando que está invertido)
        # Una forma más segura es buscar por fecha o usar una ID de venta.
        # Por ahora buscaremos por el valor de la fila.
        val = self.tree_historial.item(seleccion[0], 'values')
        fecha_sel = val[0]
        cliente_sel = val[1]

        venta_encontrada = None
        for v in self.historial:
            if v['fecha'] == fecha_sel and v['cliente'] == cliente_sel:
                venta_encontrada = v
                break

        if not venta_encontrada: return

        # Ventana emergente con detalles
        top = tk.Toplevel(self.root)
        top.title(f"Detalle de Factura - {cliente_sel}")
        top.geometry("500x400")

        lbl_info = ttk.Label(top, text=f"Detalle de Venta\nCliente: {cliente_sel}\nFecha: {fecha_sel}", font=('Helvetica', 10, 'bold'))
        lbl_info.pack(pady=10)

        tree_det = ttk.Treeview(top, columns=("nombre", "precio", "cant", "sub"), show="headings", height=10)
        tree_det.heading("nombre", text="Producto")
        tree_det.heading("precio", text="P. Unit")
        tree_det.heading("cant", text="Cant.")
        tree_det.heading("sub", text="Subtotal")

        tree_det.column("nombre", width=150)
        tree_det.column("precio", width=80)
        tree_det.column("cant", width=50)
        tree_det.column("sub", width=80)
        tree_det.pack(fill="both", expand=True, padx=10, pady=10)

        for item in venta_encontrada['items']:
            tree_det.insert("", "end", values=(item['nombre'], f"${item['precio']:.2f}", item['cantidad'], f"${item['subtotal']:.2f}"))

        lbl_total = ttk.Label(top, text=f"TOTAL (IVA Incl.): ${venta_encontrada['total']:.2f}", font=('Helvetica', 11, 'bold'))
        lbl_total.pack(pady=10)

    def configurar_pestaña_movimientos(self):
        self.tree_movimientos = ttk.Treeview(self.tab_movimientos, columns=("fecha", "prod", "tipo", "cant", "debe", "haber", "nuevo"), show="headings")
        self.tree_movimientos.heading("fecha", text="Fecha")
        self.tree_movimientos.heading("prod", text="Producto")
        self.tree_movimientos.heading("tipo", text="Tipo")
        self.tree_movimientos.heading("cant", text="Cant.")
        self.tree_movimientos.heading("debe", text="Debe (+)")
        self.tree_movimientos.heading("haber", text="Haber (-)")
        self.tree_movimientos.heading("nuevo", text="S. Final")

        self.tree_movimientos.column("fecha", width=130)
        self.tree_movimientos.column("prod", width=150)
        self.tree_movimientos.column("tipo", width=100)
        self.tree_movimientos.column("cant", width=50)
        self.tree_movimientos.column("debe", width=90)
        self.tree_movimientos.column("haber", width=90)
        self.tree_movimientos.column("nuevo", width=70)

        # Colores para Deber y Haber
        self.tree_movimientos.tag_configure('entrada', foreground='green')
        self.tree_movimientos.tag_configure('salida', foreground='red')

        scroll = ttk.Scrollbar(self.tab_movimientos, orient="vertical", command=self.tree_movimientos.yview)
        self.tree_movimientos.configure(yscrollcommand=scroll.set)

        self.tree_movimientos.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        scroll.pack(side="right", fill="y", pady=10, padx=(0,10))

        self.actualizar_tabla_movimientos()

    def actualizar_tabla_movimientos(self):
        if not hasattr(self, 'tree_movimientos'): return
        for item in self.tree_movimientos.get_children():
            self.tree_movimientos.delete(item)
        for mov in reversed(self.movimientos):
            debe = f"${mov.get('monto_debe', 0):.2f}" if mov.get('monto_debe', 0) > 0 else "-"
            haber = f"${mov.get('monto_haber', 0):.2f}" if mov.get('monto_haber', 0) > 0 else "-"

            tag = ''
            if mov.get('monto_debe', 0) > 0: tag = 'entrada'
            if mov.get('monto_haber', 0) > 0: tag = 'salida'

            self.tree_movimientos.insert("", "end", values=(
                mov['fecha'],
                mov['nombre'],
                mov['tipo'],
                mov['cantidad'],
                debe,
                haber,
                mov['nuevo']
            ), tags=(tag,))

    def actualizar_tabla_historial(self):
        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)
        for venta in reversed(self.historial): # Más recientes primero
            self.tree_historial.insert("", "end", values=(venta['fecha'], venta['cliente'], f"${venta['total']:.2f}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAutorIA(root)
    root.mainloop()
