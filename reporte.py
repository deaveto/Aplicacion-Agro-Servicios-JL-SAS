from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from tkcalendar import Calendar, DateEntry
from BaseDatos import BaseDatos
from datetime import datetime
from datetime import date
from itertools import chain
from collections import defaultdict
import pandas as pd
import os

class Reporte(Frame):
  
  DB = BaseDatos()
  
  def __init__(self, master=None):
    super().__init__(master, width=1200, height=600)
    self.master=master
    self.pack()
    self.create_widgets()
    
  def habilitarCajas(self, event):
    selectComprador = self.in_cmbCodCompradorReportes.current()
    selectContratista = self.in_cmbContratistaReportes.current()
    if selectComprador > 0:
      cod = self.in_cmbCodCompradorReportes.get()
      contra = self.DB.fBuscarDatos("Compradores", cod)
      self.in_cmbContratistaReportes.set(contra[0][3])
    if selectComprador > 0 or selectContratista > 0:
      self.in_cmbCodCompradorReportes.configure(state="disabled")
      self.in_cmbContratistaReportes.configure(state="disabled")
      self.habilitarCajasFechasReporte("normal")
  
  def habilitarCajasFechasReporte(self, estado):
    self.btnBuscarReportes.configure(state=estado)
    self.btnNuevaBusqueda.configure(state=estado)
    if estado == "normal":
      estadoCalendario = "readonly"
    else:
      estadoCalendario = estado
    self.in_calendarFechaFinalReporte.configure(state=estadoCalendario)
    self.in_calendarFechaInicioReporte.configure(state=estadoCalendario)
      
  
  def funBtnBuscarReportes(self):
    self.funBtnLimpiarReportes()
    codCompradorReportes = self.in_cmbCodCompradorReportes.get()
    fechaInicioReportes = self.in_calendarFechaInicioReporte.get_date()
    fechaFinalReportes = self.in_calendarFechaFinalReporte.get_date()
    if codCompradorReportes != "":
      if codCompradorReportes == "Codigo":
        codCompradorReportes = self.in_cmbContratistaReportes.get()
      datosReporte = self.DB.fBuscarReportes("Ventas", codCompradorReportes, fechaInicioReportes, fechaFinalReportes)
      if datosReporte != []:
        for listaVenta in datosReporte:
          self.grid.insert("", END, text=listaVenta[0],
                           value=(listaVenta[1],
                                  listaVenta[2],
                                  listaVenta[3],
                                  listaVenta[4],
                                  listaVenta[5],
                                  listaVenta[6],
                                  listaVenta[7],
                                  listaVenta[8],
                                  listaVenta[9],
                                  listaVenta[10],
                                  listaVenta[11],
                                  listaVenta[12])
                           )
      else:
        messagebox.showwarning(
          title="Busqueda Ventas",
          message="No hay ventas en este rango de fechas"
          )
    self.fTotalReportes()
    self.btnLimpiarReportes.configure(state="normal")
    self.btnGenerarReportes.configure(state="normal")
    pass
  
  def funBtnNuevaBusqueda(self):
    self.funBtnLimpiarReportes()
    self.in_cmbCodCompradorReportes.current(0)
    self.in_cmbContratistaReportes.current(0)
    self.in_calendarFechaFinalReporte.delete(0,END)
    self.in_calendarFechaInicioReporte.delete(0,END)
    self.in_cmbCodCompradorReportes.configure(state="normal")
    self.in_cmbContratistaReportes.configure(state="normal")
    self.habilitarCajasFechasReporte("disabled")
  
  def funBtnLimpiarReportes(self):
    for item in self.grid.get_children():
      self.grid.delete(item)
    self.fTotalReportes()
    messagebox.showwarning(
      title="Elementos Eliminados",
      message="Elementos de la tabla se han eliminado"
    )
    self.btnLimpiarReportes.configure(state="disabled")
    self.btnGenerarReportes.configure(state="disabled")
    pass
  
  def funBtnGenerarReportes(self):
    #self.grid.get_children()
    df_Item = pd.DataFrame()
    fechaDoc = date.today().strftime("%b-%d-%Y")
    codComprador = self.in_cmbCodCompradorReportes.get()
    if codComprador == "Codigo":
      codComprador = self.in_cmbContratistaReportes.get()
    for item in self.grid.get_children():
      dicItem = self.grid.set(item)
      df_Aux = pd.DataFrame(dicItem, index=[0])
      df_Item = pd.concat([df_Item, df_Aux])
    os.makedirs('C:/Reportes', exist_ok=True)
    df_Item.to_excel("C:/Reportes/{0}-{1}.xlsx".format(fechaDoc, codComprador),
                     sheet_name = "Reporte{0}".format(codComprador), index=False)
    self.funBtnNuevaBusqueda()
    pass
  
  def fEnterComprador(self, event):
    if self.in_cmbCodCompradorReportes.current() > 0:
      self.in_cmbCodCompradorReportes.current(self.in_cmbCodCompradorReportes.current())
      self.habilitarCajas("<<ComboboxSelected>>")
    else: messagebox.showerror(
      title="Error Comprador",
      message="El Codigo del Comprador no existe en la base de datos"
      )
  
  def fEnterContratista(self, event):
    if self.in_cmbContratistaReportes.current() > 0:
      self.in_cmbContratistaReportes.current(self.in_cmbContratistaReportes.current())
      self.habilitarCajas("<<ComboboxSelected>>")
    else: messagebox.showerror(
      title="Error Comprador",
      message="El Codigo del Comprador no existe en la base de datos"
      )
  
  def fActualizar(self):
    self.varCodCompradorReportes=self.DB.fObtenerCodigo("Compradores")
    self.in_cmbCodCompradorReportes.configure(values=self.varCodCompradorReportes)
    
    self.varContratistaReportes=self.DB.fObtenerContratista("Compradores")
    self.in_cmbContratistaReportes.configure(values=self.varContratistaReportes)
  
  def fTotalReportes(self):
    self.TotalReportes = 0
    if self.grid.get_children():
      for item in self.grid.get_children():
        dicItem = self.grid.set(item)
        self.TotalReportes += int(dicItem['Valor Total'])
    self.valorTotalReportes.configure(text="Total: "+str(self.TotalReportes))
    pass
  
  def create_widgets(self):
    frReportesP2 = Frame(self, bg="#ffb6b6")
    frReportesP2.place(x=30 ,y=30, width=1140, height=520)
    
    frDatosReportesP2 = Frame(frReportesP2, bg="#f8f7cc")
    frDatosReportesP2.place(x=20, y=30, width=1100, height=100)
    
    Label(frDatosReportesP2, text="Codigo Comprador").grid(pady=5, padx=5, row=0, column=0)
    self.varCodCompradorReportes=self.DB.fObtenerCodigo("Compradores")
    self.in_cmbCodCompradorReportes=Combobox(frDatosReportesP2, width="10", values=self.varCodCompradorReportes, postcommand=self.fActualizar)
    self.in_cmbCodCompradorReportes.grid(padx=5, row=1, column=0)
    self.in_cmbCodCompradorReportes.current(0)
    self.in_cmbCodCompradorReportes.bind("<<ComboboxSelected>>", self.habilitarCajas)
    self.in_cmbCodCompradorReportes.bind("<Return>", self.fEnterComprador)
    
    Label(frDatosReportesP2, text="Contratista").grid(pady=5, padx=5, row=0, column=1)
    self.varContratistaReportes=self.DB.fObtenerContratista("Compradores")
    self.in_cmbContratistaReportes=Combobox(frDatosReportesP2, width="10", values=self.varContratistaReportes, postcommand=self.fActualizar)
    self.in_cmbContratistaReportes.grid(padx=5, row=1, column=1)
    self.in_cmbContratistaReportes.current(0)
    self.in_cmbContratistaReportes.bind("<<ComboboxSelected>>", self.habilitarCajas)
    self.in_cmbContratistaReportes.bind("<Return>", self.fEnterContratista)
    
    Label(frDatosReportesP2, text="Fecha Inicio").grid(padx=5, pady=5, row=0, column=2)
    self.in_calendarFechaInicioReporte=DateEntry(frDatosReportesP2, date_pattern=("y-mm-dd"), width=10, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.in_calendarFechaInicioReporte.grid(padx=5, pady=5, row=1, column=2)
    
    Label(frDatosReportesP2, text="Fecha Final").grid(padx=5, pady=5, row=0, column=3)
    self.in_calendarFechaFinalReporte=DateEntry(frDatosReportesP2, date_pattern=("y-mm-dd"), width=10, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.in_calendarFechaFinalReporte.grid(padx=5, pady=5, row=1, column=3)
    
    self.btnBuscarReportes=Button(frDatosReportesP2, text="Buscar", command=self.funBtnBuscarReportes, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnBuscarReportes.grid(padx=5, row=1, column=4)
    
    self.btnNuevaBusqueda=Button(frDatosReportesP2, text="Neva Busqueda", command=self.funBtnNuevaBusqueda, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnNuevaBusqueda.grid(padx=5, row=1, column=5)
    
    frTablaReportesP2 = Frame(frReportesP2, bg="#ccedf8")
    frTablaReportesP2.place(x=20, y=150, width=1100, height=350)
    
    frBtnLimpiarReportesP2 = Frame(frTablaReportesP2, bg="#C1FFBE")
    frBtnLimpiarReportesP2.grid(padx=5, pady=5,row=0, column=0, sticky=E)
    
    self.btnLimpiarReportes=Button(frBtnLimpiarReportesP2, text="Limpiar Tabla", command=self.funBtnLimpiarReportes, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnLimpiarReportes.grid(padx=5, pady=5,row=0, column=0, sticky=W)
    
    self.TotalReportes = 0
    self.valorTotalReportes = Label(frTablaReportesP2, text="Total: "+str(self.TotalReportes))
    self.valorTotalReportes.grid(pady=5, padx=5, row=2, column=0, sticky=E)
    
    self.btnGenerarReportes=Button(frTablaReportesP2, text="Generar Reporte", command=self.funBtnGenerarReportes, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnGenerarReportes.grid(padx=5, pady=5,row=3, column=0, sticky=E)
    
    columnas = ["Cod Comprador", "Nombre", "Apellido", "Contratista", "Cod Producto", "Producto", "Cantidad", "Fecha", "Valor Unitario", "Valor Total", "Descripcion", "Responsable"]
    self.grid=ttk.Treeview(frTablaReportesP2, columns=columnas)
    
    self.grid.column("#0", width=45, anchor=CENTER)
    self.grid.heading("#0", text="Item", anchor=CENTER)
    for col in columnas:
      self.grid.column(col, width=85, anchor=CENTER)
      self.grid.heading(col, text=col, anchor=CENTER)

    self.grid.grid(padx=5, pady=5,row=1, column=0, sticky=E+W)
    
    scrollBar = Scrollbar(frTablaReportesP2, orient=VERTICAL)
    scrollBar.grid(padx=0, pady=5,row=1, column=1, sticky=S+N+E+W)
    self.grid.config(yscrollcommand=scrollBar.set)
    scrollBar.config(command=self.grid.yview) 