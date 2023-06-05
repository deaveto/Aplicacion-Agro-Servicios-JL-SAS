from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from BaseDatos import BaseDatos
from datetime import datetime
from ventanaNuevoComprador import *

class Ventana(Frame):
  
  DB = BaseDatos()
  
  def __init__(self, master=None):
    super().__init__(master, width=1200, height=600)
    self.master=master
    self.pack()
    self.create_widgets()
    
  def funBtnVentasP1(self):
    pass
  
  def funBtnAdicionarVentas(self):
    index = len(self.grid.get_children())+1
    codComprador = self.in_cmbCodCompradorVentas.get()
    codProducto = self.in_cmbCodProductoVentas.get()
    cant = self.in_TxtCantidadVentas.get()
    datosComprador = self.DB.fObtenerDatos("Compradores", codComprador)
    datosProducto = self.DB.fObtenerDatos("Productos", codProducto)
    self.grid.insert("",END,text=index, value=(codComprador,
                                               datosComprador[1],
                                               datosComprador[2],
                                               datosComprador[3],
                                               codProducto,
                                               datosProducto[1],
                                               cant,
                                               datetime.now(),
                                               datosProducto[2],
                                               int(datosProducto[2])*int(cant),
                                               self.in_TxtDescripcionVentas.get()
                                               )
                     )
    self.fTotal()
    self.in_cmbCodProductoVentas.current(0)
    self.in_TxtCantidadVentas.delete(0,END)
    self.in_TxtDescripcionVentas.delete(0,END)
    self.habilitarBtnBorradoVentas("normal")
    self.in_cmbCodProductoVentas.focus()
  
  def funBtnNuevoVentas(self):
    self.funBtnLimpiarVentas()
    self.in_cmbCodProductoVentas.current(0)
    self.in_cmbCodCompradorVentas.current(0)
    self.in_TxtCantidadVentas.delete(0,END)
    self.in_TxtDescripcionVentas.delete(0,END)
    self.in_cmbCodCompradorVentas.configure(state="normal")
    self.habilitarCajasDatosVentas("disabled")
  
  def funBtnNuevoCompradorVentas(self):
    VentanaNuevoComprador()
    pass
  
  def funBtnBuscarVentas(self):
    codProducto = self.in_cmbCodProductoVentas.get()
    if codProducto != "":
      datosProducto = self.DB.fBuscarDatos("Productos", codProducto.upper())
      if datosProducto != []:
        textProducto = ""
        for produ in datosProducto:
          textProducto=textProducto+"Codigo: "+produ[0]+"\n"+"Nombre: "+produ[1]+"\n"+"Precio: "+produ[2]+"\n\n\n"
        messagebox.showinfo(
          title="Elemeno Buscado",
            message=textProducto
        )
        self.in_cmbCodProductoVentas.delete(0,END)
      else:
        messagebox.showwarning(
          title="Buscar Item",
          message="No se encontro Item")
    else:
      messagebox.showwarning(
        title="Buscar Item",
          message="Porfavor escriba un Item")
  
  def funBtnLimpiarVentas(self):
    for item in self.grid.get_children():
      self.grid.delete(item)
    self.fTotal()
    messagebox.showwarning(
      title="Elementos Eliminados",
      message="Elementos de la tabla se han eliminado"
    )
    self.habilitarBtnBorradoVentas("disabled")
    
  def funBtnLimpiarUltimoVentas(self):
    ultimo = ""
    for item in self.grid.get_children():
      ultimo = item
    self.grid.delete(ultimo)
    self.fTotal()
    self.fVerificarItemTabla()
    
  def funBtnLimpiarItemVentas(self):
    select = self.grid.focus()
    idItem = self.grid.item(select, "text")
    if idItem != "":
      r = messagebox.askquestion(title="Eliminar Item",
                             message=f"Deseas Eliminar el Item numero {idItem}")
      if r == messagebox.YES:
        self.grid.delete(select)
      else:
        pass
    else:
      messagebox.showwarning(
        title="Eliminar Item",
        message="Debes de seleccionar un Item de la tabla")
    self.fTotal()
    self.fVerificarItemTabla()
    
  def fVerificarItemTabla (self):
    if self.grid.get_children():
      pass
    else:
      self.habilitarBtnBorradoVentas("disabled")
    
  def funBtnGuardarVentas(self):
    r = messagebox.askquestion(title="Guardar Ventas",
                             message=f"Deseas Guardar los Item de la Ventas")
    if r == messagebox.YES:
      ventas = self.grid.get_children()
      for item in ventas:
        itemVenta = self.grid.item(item, "text")
        datosVenta = self.grid.item(item, "values")
        datosVenta = [itemVenta, *datosVenta]
        self.DB.fAgregarDatos("Ventas", datosVenta)
        self.DB.fDescontarCantidad("Productos", datosVenta[5], datosVenta[7])
      self.funBtnNuevoVentas()
    else:
      pass
  
  def habilitarCajas(self, event):
    selectComprador = self.in_cmbCodCompradorVentas.current()
    if selectComprador > 0:
      self.in_cmbCodCompradorVentas.configure(state="disabled")
      self.habilitarCajasDatosVentas("normal")
      
  def habilitarCajasDatosVentas(self, estado):
    self.in_cmbCodProductoVentas.configure(state=estado)
    self.in_TxtCantidadVentas.configure(state=estado)
    self.in_TxtDescripcionVentas.configure(state=estado)
    self.btnAdicionarVentas.configure(state=estado)
    self.btnNuevoVentas.configure(state=estado)
  
  def habilitarBtnBorradoVentas(self, estado):
    self.btnLimpiarVentas.configure(state=estado)
    self.btnLimpiarUltimoVentas.configure(state=estado)
    self.btnLimpiarItemVentas.configure(state=estado)
    self.btnGuardarVentas.configure(state=estado)
      
  def fEnterComprador(self, event):
    if self.in_cmbCodCompradorVentas.current() > 0:
      self.in_cmbCodCompradorVentas.current(self.in_cmbCodCompradorVentas.current())
      self.habilitarCajas("<<ComboboxSelected>>")
      self.in_cmbCodProductoVentas.focus()
      self.in_cmbCodProductoVentas.delete(0,END)
    else: messagebox.showerror(
      title="Error Comprador",
      message="El Codigo del Comprador no existe en la base de datos"
      )
  
  def fEnterProducto(self, event):
    if self.in_cmbCodProductoVentas.current() > 0:
      self.in_TxtCantidadVentas.focus()
    else:messagebox.showerror(
      title="Error Producto",
      message="El Codigo del Producto no existe en la base de datos"
      )
  
  def fEnterCantidad(self, event):
    if self.in_TxtCantidadVentas.get().isdigit():
      self.in_TxtDescripcionVentas.focus()
    else:messagebox.showerror(
      title="Error Cantidad",
      message="La cantidad es incorrecta"
      )
  
  def fEnterDescripcion(self, event):
    self.funBtnAdicionarVentas()
    self.in_cmbCodProductoVentas.delete(0,END)
  
  def limpiarTabla(self):
    print(self.grid.get_children())
    
  def fTotal(self):
    self.Total = 0
    if self.grid.get_children():
      for item in self.grid.get_children():
        dicItem = self.grid.set(item)
        self.Total += int(dicItem['Valor Total'])
    self.valorTotal.configure(text="Total: "+str(self.Total))
    
  def fActualizar(self):
    self.varCodCompradorVentas=self.DB.fObtenerCodigo("Compradores")
    self.in_cmbCodCompradorVentas.configure(values=self.varCodCompradorVentas)
    
    self.varCodProductoVentas=self.DB.fObtenerCodigo("Productos")
    self.in_cmbCodProductoVentas.configure(values=self.varCodProductoVentas)
    
  def create_widgets(self):
    frVentasP1 = Frame(self, bg="#ffb6b6")
    frVentasP1.place(x=30 ,y=30, width=1140, height=520)
    
    frDatosVentasP1 = Frame(frVentasP1, bg="#f8f7cc")
    frDatosVentasP1.place(x=20, y=30, width=1100, height=100)
    
    Label(frDatosVentasP1, text="Codigo Comprador").grid(pady=5, padx=5, row=0, column=0)
    self.varCodCompradorVentas=self.DB.fObtenerCodigo("Compradores")
    self.in_cmbCodCompradorVentas=Combobox(frDatosVentasP1, width="10", values=self.varCodCompradorVentas, postcommand=self.fActualizar)
    self.in_cmbCodCompradorVentas.grid(padx=5, row=1, column=0)
    self.in_cmbCodCompradorVentas.current(0)
    self.in_cmbCodCompradorVentas.bind("<<ComboboxSelected>>", self.habilitarCajas)
    self.in_cmbCodCompradorVentas.bind("<Return>", self.fEnterComprador)
    self.btnNuevoCompradorVentas=Button(frDatosVentasP1, text="Nuevo comprador", command=self.funBtnNuevoCompradorVentas, bg="#f87c7c", fg="#ffffff")
    self.btnNuevoCompradorVentas.grid(pady=5, padx=5, row=2, column=0)
    
    Label(frDatosVentasP1, text="Codigo Producto").grid(pady=5, padx=5, row=0, column=1)
    self.varCodProductoVentas=self.DB.fObtenerCodigo("Productos")
    self.in_cmbCodProductoVentas=Combobox(frDatosVentasP1, width="10", values=self.varCodProductoVentas, state="disabled", postcommand=self.fActualizar)
    self.in_cmbCodProductoVentas.grid(padx=5, row=1, column=1)
    self.in_cmbCodProductoVentas.current(0)
    self.in_cmbCodProductoVentas.bind("<Return>", self.fEnterProducto)
    self.btnBuscarVentas=Button(frDatosVentasP1, text="Buscar", command=self.funBtnBuscarVentas, bg="#f87c7c", fg="#ffffff")
    self.btnBuscarVentas.grid(pady=5, padx=5, row=2, column=1)
    
    Label(frDatosVentasP1, text="Cantidad").grid(pady=5, padx=5, row=0, column=2)
    self.in_TxtCantidadVentas=Entry(frDatosVentasP1, width=10, state="disabled")
    self.in_TxtCantidadVentas.grid(padx=5, row=1, column=2)
    self.in_TxtCantidadVentas.bind("<Return>", self.fEnterCantidad)
    
    Label(frDatosVentasP1, text="Descripcion").grid(pady=5, padx=5, row=0, column=3)
    self.in_TxtDescripcionVentas=Entry(frDatosVentasP1, width=10, state="disabled")
    self.in_TxtDescripcionVentas.grid(padx=5, row=1, column=3)
    self.in_TxtDescripcionVentas.bind("<Return>", self.fEnterDescripcion)
    
    self.btnAdicionarVentas=Button(frDatosVentasP1, text="Adicionar", command=self.funBtnAdicionarVentas, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnAdicionarVentas.grid(padx=5, row=1, column=4)
    
    self.btnNuevoVentas=Button(frDatosVentasP1, text="Neva Venta", command=self.funBtnNuevoVentas, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnNuevoVentas.grid(padx=5, row=1, column=5)
    
    frTablaVentasP1 = Frame(frVentasP1, bg="#ccedf8")
    frTablaVentasP1.place(x=20, y=150, width=1100, height=350)
    
    frBtnLimpiarVentasP1 = Frame(frTablaVentasP1, bg="#C1FFBE")
    frBtnLimpiarVentasP1.grid(padx=5, pady=5,row=0, column=0, sticky=E)
    
    self.btnLimpiarVentas=Button(frBtnLimpiarVentasP1, text="Borrar Tabla", command=self.funBtnLimpiarVentas, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnLimpiarVentas.grid(padx=5, pady=5,row=0, column=0, sticky=W)
    
    self.btnLimpiarUltimoVentas=Button(frBtnLimpiarVentasP1, text="Borrar Ultimo", command=self.funBtnLimpiarUltimoVentas, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnLimpiarUltimoVentas.grid(padx=5, pady=5,row=0, column=1, sticky=E)
    
    self.btnLimpiarItemVentas=Button(frBtnLimpiarVentasP1, text="Borrar Item", command=self.funBtnLimpiarItemVentas, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnLimpiarItemVentas.grid(padx=5, pady=5,row=0, column=2, sticky=E)
    
    self.Total = 0
    self.valorTotal = Label(frTablaVentasP1, text="Total: "+str(self.Total))
    self.valorTotal.grid(pady=5, padx=5, row=2, column=0, sticky=E)
    
    self.btnGuardarVentas=Button(frTablaVentasP1, text="Guardar", command=self.funBtnGuardarVentas, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnGuardarVentas.grid(padx=5, pady=5,row=3, column=0, sticky=E)
    
    columnas = ["Cod Comprador", "Nombre", "Apellido", "Contratista", "Cod Producto", "Producto", "Cantidad", "Fecha", "Valor Unitario", "Valor Total", "Descripcion"]
    self.grid=ttk.Treeview(frTablaVentasP1, columns=columnas)
    
    self.grid.column("#0", width=40, anchor=CENTER)
    self.grid.heading("#0", text="Item", anchor=CENTER)
    for col in columnas:
      self.grid.column(col, width=93, anchor=CENTER)
      self.grid.heading(col, text=col, anchor=CENTER)

    self.grid.grid(padx=5, pady=5,row=1, column=0, sticky=E+W)
    
    scrollBar = Scrollbar(frTablaVentasP1, orient=VERTICAL)
    scrollBar.grid(padx=0, pady=5,row=1, column=1, sticky=S+N+E+W)
    self.grid.config(yscrollcommand=scrollBar.set)
    scrollBar.config(command=self.grid.yview)