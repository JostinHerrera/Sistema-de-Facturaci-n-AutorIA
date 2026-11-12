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

        # Pestaña 5: Clientes
        self.tab_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_clientes, text="Gestión de Clientes")
        self.configurar_pestaña_clientes()

        # Pestaña 6: Análisis Financiero
        self.tab_analisis = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_analisis, text="Análisis Financiero")
        self.configurar_pestaña_analisis()

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
        if hasattr(self, 'tree_analisis'):
            self.actualizar_analisis()

    def cargar_datos(self):
        """Carga el inventario y el historial desde un archivo JSON o usa valores por defecto."""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.inventario = datos.get("inventario", {})
                    self.historial = datos.get("historial", [])
                    self.movimientos = datos.get("movimientos", [])
                    self.clientes = datos.get("clientes", {})
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
        self.clientes = {}
        self.guardar_datos()

    def guardar_datos(self):
        """Guarda el estado actual en el archivo JSON."""
        datos = {
            "inventario": self.inventario,
            "historial": self.historial,
            "movimientos": self.movimientos,
            "clientes": self.clientes
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
        self.combo_clientes = ttk.Combobox(frame_cliente, width=30, state="readonly")
        self.combo_clientes.grid(row=0, column=1, sticky="w", padx=5)
        self.actualizar_combo_clientes()

        ttk.Label(frame_cliente, text="Contacto:").grid(row=0, column=2, sticky="w", padx=5)
        self.entry_contacto_factura = ttk.Entry(frame_cliente, width=25)
        self.entry_contacto_factura.grid(row=0, column=3, sticky="w", padx=5)

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
        self.combo_clientes.set('')
        self.entry_contacto_factura.delete(0, tk.END)
        self.actualizar_total_factura()

    def finalizar_factura(self):
        cliente_id = self.combo_clientes.get().split(" | ")[0] if " | " in self.combo_clientes.get() else ""
        if not cliente_id or cliente_id not in self.clientes:
            messagebox.showerror("Error", "Debe seleccionar un cliente válido.")
            return

        cliente_info = self.clientes[cliente_id]
        cliente_nombre = cliente_info['empresa']
        contacto = self.entry_contacto_factura.get().strip()

        if not self.items_factura_actual:
            messagebox.showerror("Error", "La factura está vacía.")
            return

        # Confirmar y actualizar inventario
        total_venta = sum(item['subtotal'] for item in self.items_factura_actual) * 1.15
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Registro para historial
        venta = {
            "fecha": fecha,
            "cliente": cliente_nombre,
            "cliente_id": cliente_id,
            "contacto": contacto,
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
        self.actualizar_analisis() # Actualizar análisis financiero

        # Mostrar resumen tipo factura
        mensaje_factura = f"FACTURA: AutorIA\nFECHA: {fecha}\nCLIENTE: {cliente_nombre}\n"
        if contacto:
            mensaje_factura += f"CONTACTO: {contacto}\n"
        mensaje_factura += "="*30 + "\n"
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
        # Frame de Filtros
        frame_filtro = ttk.Frame(self.tab_historial, padding=5)
        frame_filtro.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_filtro, text="Empresa:").pack(side="left", padx=5)
        self.combo_filtro_cliente = ttk.Combobox(frame_filtro, state="readonly", width=25)
        self.combo_filtro_cliente.pack(side="left", padx=5)
        self.combo_filtro_cliente.bind("<<ComboboxSelected>>", lambda e: self.actualizar_tabla_historial())

        ttk.Label(frame_filtro, text="Fecha (AAAA-MM-DD o AAAA-MM):").pack(side="left", padx=5)
        self.entry_filtro_fecha = ttk.Entry(frame_filtro, width=15)
        self.entry_filtro_fecha.pack(side="left", padx=5)
        self.entry_filtro_fecha.bind("<KeyRelease>", lambda e: self.actualizar_tabla_historial())

        ttk.Button(frame_filtro, text="Limpiar Filtros", command=self.limpiar_filtro_historial).pack(side="left", padx=10)

        # Instrucciones
        ttk.Label(self.tab_historial, text="Doble clic en una venta para ver el detalle de productos", font=('Helvetica', 9, 'italic')).pack(pady=2)

        self.tree_historial = ttk.Treeview(self.tab_historial, columns=("fecha", "cliente", "total"), show="headings")
        self.tree_historial.heading("fecha", text="Fecha y Hora")
        self.tree_historial.heading("cliente", text="Cliente / Empresa")
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

    def limpiar_filtro_historial(self):
        self.combo_filtro_cliente.set("Todos")
        self.entry_filtro_fecha.delete(0, tk.END)
        self.actualizar_tabla_historial()

    def actualizar_combo_filtro_historial(self):
        if not hasattr(self, 'combo_filtro_cliente'): return
        empresas = set(v.get('cliente', '') for v in self.historial if v.get('cliente'))
        # También incluir empresas registradas en clientes por si acaso
        for cli in self.clientes.values():
            if cli.get('empresa'):
                empresas.add(cli['empresa'])
        lista = ["Todos"] + sorted(list(empresas))
        val_actual = self.combo_filtro_cliente.get()
        self.combo_filtro_cliente['values'] = lista
        if val_actual in lista:
            self.combo_filtro_cliente.set(val_actual)
        else:
            self.combo_filtro_cliente.set("Todos")

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

        contacto_text = f"\nContacto: {venta_encontrada.get('contacto', 'N/A')}" if venta_encontrada.get('contacto') else ""
        lbl_info = ttk.Label(top, text=f"Detalle de Venta\nCliente: {cliente_sel}{contacto_text}\nFecha: {fecha_sel}", font=('Helvetica', 10, 'bold'))
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
        if not hasattr(self, 'tree_historial'): return
        self.actualizar_combo_filtro_historial()

        filtro_empresa = self.combo_filtro_cliente.get() if hasattr(self, 'combo_filtro_cliente') else "Todos"
        filtro_fecha = self.entry_filtro_fecha.get().strip() if hasattr(self, 'entry_filtro_fecha') else ""

        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)

        for venta in reversed(self.historial): # Más recientes primero
            if filtro_empresa != "Todos" and venta.get('cliente') != filtro_empresa:
                continue
            if filtro_fecha and not venta.get('fecha', '').startswith(filtro_fecha):
                continue
            self.tree_historial.insert("", "end", values=(venta['fecha'], venta['cliente'], f"${venta['total']:.2f}"))

    # --- PESTAÑA: CLIENTES ---
    def configurar_pestaña_clientes(self):
        # Frame para el formulario de clientes
        frame_form = ttk.LabelFrame(self.tab_clientes, text="Datos del Cliente (Empresa)", padding=10)
        frame_form.pack(side="top", fill="x", padx=10, pady=10)

        # Campos solicitados: correo, direccion, telefono, nombre de la empresa e identificacion fiscal
        ttk.Label(frame_form, text="ID Fiscal (RUC/NIT):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.entry_cli_id = ttk.Entry(frame_form, width=20)
        self.entry_cli_id.grid(row=0, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Nombre Empresa:").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        self.entry_cli_empresa = ttk.Entry(frame_form, width=30)
        self.entry_cli_empresa.grid(row=0, column=3, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Correo:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.entry_cli_correo = ttk.Entry(frame_form, width=30)
        self.entry_cli_correo.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Teléfono:").grid(row=1, column=2, padx=5, pady=2, sticky="w")
        self.entry_cli_telefono = ttk.Entry(frame_form, width=20)
        self.entry_cli_telefono.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        ttk.Label(frame_form, text="Dirección:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.entry_cli_direccion = ttk.Entry(frame_form, width=50)
        self.entry_cli_direccion.grid(row=2, column=1, columnspan=3, padx=5, pady=2, sticky="w")

        # Botones de acción para clientes
        frame_btns_cli = ttk.Frame(frame_form)
        frame_btns_cli.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(frame_btns_cli, text="Guardar Cliente", command=self.guardar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_btns_cli, text="Eliminar Seleccionado", command=self.eliminar_cliente).pack(side="left", padx=5)
        ttk.Button(frame_btns_cli, text="Limpiar Formulario", command=self.limpiar_form_cliente).pack(side="left", padx=5)

        # Tabla de clientes
        self.tree_clientes = ttk.Treeview(self.tab_clientes, columns=("id", "empresa", "correo", "telefono", "direccion"), show="headings")
        self.tree_clientes.heading("id", text="ID Fiscal")
        self.tree_clientes.heading("empresa", text="Empresa")
        self.tree_clientes.heading("correo", text="Correo")
        self.tree_clientes.heading("telefono", text="Teléfono")
        self.tree_clientes.heading("direccion", text="Dirección")

        self.tree_clientes.column("id", width=100)
        self.tree_clientes.column("empresa", width=180)
        self.tree_clientes.column("correo", width=150)
        self.tree_clientes.column("telefono", width=100)
        self.tree_clientes.column("direccion", width=220)
        self.tree_clientes.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_clientes.bind("<<TreeviewSelect>>", self.cargar_cliente_seleccionado)
        self.actualizar_tabla_clientes()

    def actualizar_tabla_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)

        for id_fiscal, datos in sorted(self.clientes.items()):
            self.tree_clientes.insert("", "end", values=(
                id_fiscal,
                datos.get('empresa', ''),
                datos.get('correo', ''),
                datos.get('telefono', ''),
                datos.get('direccion', '')
            ))
        self.actualizar_combo_clientes()

    def actualizar_combo_clientes(self):
        if not hasattr(self, 'combo_clientes'): return
        lista = [f"{id} | {datos['empresa']}" for id, datos in self.clientes.items()]
        self.combo_clientes['values'] = lista
        if lista and not self.combo_clientes.get():
            self.combo_clientes.current(0)

    def cargar_cliente_seleccionado(self, event):
        seleccion = self.tree_clientes.selection()
        if not seleccion: return

        item_data = self.tree_clientes.item(seleccion[0], 'values')
        id_fiscal = item_data[0]
        datos = self.clientes.get(id_fiscal, {})

        self.limpiar_form_cliente()
        self.entry_cli_id.insert(0, id_fiscal)
        self.entry_cli_empresa.insert(0, datos.get('empresa', ''))
        self.entry_cli_correo.insert(0, datos.get('correo', ''))
        self.entry_cli_telefono.insert(0, datos.get('telefono', ''))
        self.entry_cli_direccion.insert(0, datos.get('direccion', ''))

    def limpiar_form_cliente(self):
        self.entry_cli_id.delete(0, tk.END)
        self.entry_cli_empresa.delete(0, tk.END)
        self.entry_cli_correo.delete(0, tk.END)
        self.entry_cli_telefono.delete(0, tk.END)
        self.entry_cli_direccion.delete(0, tk.END)

    def guardar_cliente(self):
        id_fiscal = self.entry_cli_id.get().strip()
        empresa = self.entry_cli_empresa.get().strip()
        correo = self.entry_cli_correo.get().strip()
        telefono = self.entry_cli_telefono.get().strip()
        direccion = self.entry_cli_direccion.get().strip()

        if not id_fiscal or not empresa:
            messagebox.showerror("Error", "ID Fiscal y Nombre de Empresa son obligatorios.")
            return

        self.clientes[id_fiscal] = {
            "empresa": empresa,
            "correo": correo,
            "telefono": telefono,
            "direccion": direccion
        }
        self.guardar_datos()
        self.actualizar_tabla_clientes()
        self.limpiar_form_cliente()
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")

    def eliminar_cliente(self):
        seleccion = self.tree_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente de la tabla.")
            return

        item_data = self.tree_clientes.item(seleccion[0], 'values')
        id_fiscal = item_data[0]

        if messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al cliente '{item_data[1]}'?"):
            if id_fiscal in self.clientes:
                del self.clientes[id_fiscal]
                self.guardar_datos()
                self.actualizar_tabla_clientes()
                self.limpiar_form_cliente()

    # --- PESTAÑA: ANÁLISIS FINANCIERO ---
    def configurar_pestaña_analisis(self):
        # Frame superior: Tarjetas / Resumen KPI
        frame_kpis = ttk.LabelFrame(self.tab_analisis, text="Resumen Financiero Global", padding=15)
        frame_kpis.pack(fill="x", padx=10, pady=10)

        # Configurar 3 columnas iguales
        frame_kpis.columnconfigure(0, weight=1)
        frame_kpis.columnconfigure(1, weight=1)
        frame_kpis.columnconfigure(2, weight=1)

        # Card 1: Entró (Ingresos)
        f_ingresos = ttk.Frame(frame_kpis, padding=10, relief="solid")
        f_ingresos.grid(row=0, column=0, padx=10, sticky="ew")
        ttk.Label(f_ingresos, text="Total Entró (Ventas)", font=('Helvetica', 10, 'bold')).pack()
        self.lbl_total_ingresos = ttk.Label(f_ingresos, text="$0.00", font=('Helvetica', 14, 'bold'), foreground="green")
        self.lbl_total_ingresos.pack(pady=5)

        # Card 2: Salió (Egresos)
        f_egresos = ttk.Frame(frame_kpis, padding=10, relief="solid")
        f_egresos.grid(row=0, column=1, padx=10, sticky="ew")
        ttk.Label(f_egresos, text="Total Salió (Inversión/Stock)", font=('Helvetica', 10, 'bold')).pack()
        self.lbl_total_egresos = ttk.Label(f_egresos, text="$0.00", font=('Helvetica', 14, 'bold'), foreground="red")
        self.lbl_total_egresos.pack(pady=5)

        # Card 3: Balance Neto
        f_balance = ttk.Frame(frame_kpis, padding=10, relief="solid")
        f_balance.grid(row=0, column=2, padx=10, sticky="ew")
        ttk.Label(f_balance, text="Balance Neto Global", font=('Helvetica', 10, 'bold')).pack()
        self.lbl_total_balance = ttk.Label(f_balance, text="$0.00", font=('Helvetica', 14, 'bold'), foreground="blue")
        self.lbl_total_balance.pack(pady=5)

        # Frame inferior: Tabla por Meses
        frame_tabla = ttk.LabelFrame(self.tab_analisis, text="Desglose Mensual (Entradas vs Salidas)", padding=10)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree_analisis = ttk.Treeview(frame_tabla, columns=("mes", "ingresos", "egresos", "balance", "num_ventas"), show="headings")
        self.tree_analisis.heading("mes", text="Año - Mes")
        self.tree_analisis.heading("ingresos", text="Entró (Ventas)")
        self.tree_analisis.heading("egresos", text="Salió (Compras/Stock)")
        self.tree_analisis.heading("balance", text="Balance Neto")
        self.tree_analisis.heading("num_ventas", text="Cant. Ventas")

        self.tree_analisis.column("mes", width=120, anchor="center")
        self.tree_analisis.column("ingresos", width=150, anchor="e")
        self.tree_analisis.column("egresos", width=150, anchor="e")
        self.tree_analisis.column("balance", width=150, anchor="e")
        self.tree_analisis.column("num_ventas", width=100, anchor="center")

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_analisis.yview)
        self.tree_analisis.configure(yscrollcommand=scroll.set)

        self.tree_analisis.pack(side="left", fill="both", expand=True, padx=(5,0), pady=5)
        scroll.pack(side="right", fill="y", pady=5, padx=(0,5))

        self.actualizar_analisis()

    def actualizar_analisis(self):
        if not hasattr(self, 'tree_analisis'): return

        for item in self.tree_analisis.get_children():
            self.tree_analisis.delete(item)

        # Recopilar datos por mes YYYY-MM
        datos_meses = {}

        # Procesar Ventas (Entró)
        for venta in self.historial:
            fecha_str = venta.get('fecha', '')
            if len(fecha_str) >= 7:
                mes = fecha_str[:7]
                if mes not in datos_meses:
                    datos_meses[mes] = {'ingresos': 0.0, 'egresos': 0.0, 'ventas': 0}
                datos_meses[mes]['ingresos'] += venta.get('total', 0.0)
                datos_meses[mes]['ventas'] += 1

        # Procesar Movimientos de Inventario (Salió - Inversión/Entradas de stock)
        for mov in self.movimientos:
            fecha_str = mov.get('fecha', '')
            if len(fecha_str) >= 7:
                mes = fecha_str[:7]
                if mes not in datos_meses:
                    datos_meses[mes] = {'ingresos': 0.0, 'egresos': 0.0, 'ventas': 0}
                datos_meses[mes]['egresos'] += mov.get('monto_debe', 0.0)

        total_ingresos_global = 0.0
        total_egresos_global = 0.0

        for mes in sorted(datos_meses.keys(), reverse=True):
            ing = datos_meses[mes]['ingresos']
            egr = datos_meses[mes]['egresos']
            bal = ing - egr
            cant_v = datos_meses[mes]['ventas']

            total_ingresos_global += ing
            total_egresos_global += egr

            self.tree_analisis.insert("", "end", values=(
                mes,
                f"${ing:.2f}",
                f"${egr:.2f}",
                f"${bal:.2f}",
                cant_v
            ))

        balance_global = total_ingresos_global - total_egresos_global
        self.lbl_total_ingresos.config(text=f"${total_ingresos_global:.2f}")
        self.lbl_total_egresos.config(text=f"${total_egresos_global:.2f}")

        if balance_global >= 0:
            self.lbl_total_balance.config(text=f"${balance_global:.2f}", foreground="green")
        else:
            self.lbl_total_balance.config(text=f"${balance_global:.2f}", foreground="red")

    def actualizar_tabla_historial(self):
        if not hasattr(self, 'tree_historial'): return
        self.actualizar_combo_filtro_historial()

        filtro_empresa = self.combo_filtro_cliente.get() if hasattr(self, 'combo_filtro_cliente') else "Todos"
        filtro_fecha = self.entry_filtro_fecha.get().strip() if hasattr(self, 'entry_filtro_fecha') else ""

        for item in self.tree_historial.get_children():
            self.tree_historial.delete(item)

        for venta in reversed(self.historial): # Más recientes primero
            if filtro_empresa != "Todos" and venta.get('cliente') != filtro_empresa:
                continue
            if filtro_fecha and not venta.get('fecha', '').startswith(filtro_fecha):
                continue
            self.tree_historial.insert("", "end", values=(venta['fecha'], venta['cliente'], f"${venta['total']:.2f}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaAutorIA(root)
    root.mainloop()
