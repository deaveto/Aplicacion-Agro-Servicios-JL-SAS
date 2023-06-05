from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from BaseDatos import BaseDatos
from datetime import datetime

class VentanaNuevoComprador(Frame):
  
  DB = BaseDatos()
  
  def __init__(self):
    self.ventanaNuevoComprador = Toplevel()
    self.ventanaNuevoComprador.geometry("500x300")
    self.ventanaNuevoComprador.title("Nuevo Comprador")
    self.create_widgets()
    
  def fHabilitarInput(self, estado):
    self.in_TxtNombreNuevoComprador.configure(state=estado)
    self.in_TxtApellidoNuevoComprador.configure(state=estado)
    self.in_TxtContratistaNuevoComprador.configure(state=estado)
    self.btnGuardarNuevoComprador.configure(state=estado)
    pass
    
  def fEnterCodigoNuevoComprador(self, event): 
    codigo=self.in_TxtCodigoNuevoComprador.get()
    if codigo.isdigit() and (len(codigo) == 8 or len(codigo) == 10):
      self.fHabilitarInput("normal")
      self.in_TxtNombreNuevoComprador.focus()
    else:
      messagebox.showerror(
      title="Error Codigo",
      message="El Numero de Identificacion no es correcto"
      )
      self.ventanaNuevoComprador.focus()
  
  def fEnterNombreNuevoComprador(self, event):
    self.in_TxtApellidoNuevoComprador.focus()
    pass
  
  def fEnterApellidoNuevoComprador(self, event):
    self.in_TxtContratistaNuevoComprador.focus()
    pass
  
  def fEnterContratistaNuevoComprador(self, event):
    self.funBtnGuardarNuevoComprador()
    pass
  
  def funBtnGuardarNuevoComprador(self):
    codigo=self.in_TxtCodigoNuevoComprador.get()
    nombre=self.in_TxtNombreNuevoComprador.get()
    apellido=self.in_TxtApellidoNuevoComprador.get()
    contratista=self.in_TxtContratistaNuevoComprador.get()
    listDatosNuevoComprador = []
    if codigo.isdigit() and (len(codigo) == 8 or len(codigo) == 10):
      listDatosNuevoComprador.append(codigo)
    else:
      messagebox.showerror(
      title="Error Codigo",
      message="El Numero de Identificacion no es correcto"
      )
      self.ventanaNuevoComprador.focus()
    if nombre != "" and len(nombre) > 3:
      listDatosNuevoComprador.append(nombre.capitalize())
    else:
      messagebox.showerror(
      title="Error Nombre",
      message="El Nombre es incorrecto"
      )
      self.ventanaNuevoComprador.focus()
    if apellido != "" and len(apellido) > 3:
      listDatosNuevoComprador.append(apellido.capitalize())
    else:
      messagebox.showerror(
      title="Error Apellido",
      message="El Apellido es incorrecto"
      )
      self.ventanaNuevoComprador.focus()
    if contratista != "":
      listDatosNuevoComprador.append(contratista.upper())
    else:
      messagebox.showerror(
      title="Error Contratista",
      message="El Contratista es incorrecto"
      )
      self.ventanaNuevoComprador.focus()
    if len(listDatosNuevoComprador) == 4:
      r = messagebox.askquestion(title="Agregar Comprador",
                                 message=f"""Desea agregar este nuevo Comprador
                                 \n Num ID: {listDatosNuevoComprador[0]}
                                 \n Nombre: {listDatosNuevoComprador[1]}
                                 \n Apellido: {listDatosNuevoComprador[2]}
                                 \n Contratista: {listDatosNuevoComprador[3]}""")
      if r == messagebox.YES:
        self.DB.fAgregarDatos("Compradores", listDatosNuevoComprador)
        self.ventanaNuevoComprador.destroy()
      else:
        self.ventanaNuevoComprador.focus()
    else:
      messagebox.showerror(
      title="Error Datos",
      message="Los Datos del Nuevo Comprador son incorrectos"
      )
      self.ventanaNuevoComprador.focus()
  
  def funBtnCancelarNuevoComprador(self):
    r = messagebox.askquestion(title="Agregar Comprador",
                                 message=f"Desea Cancelar la operacion del Nuevo Comprador")
    if r == messagebox.YES:
      self.ventanaNuevoComprador.destroy()
    else:
      self.ventanaNuevoComprador.focus()
      
  
  def create_widgets(self):
    frNuevoComprador = Frame(self.ventanaNuevoComprador, bg="#ffb6b6")
    frNuevoComprador.grid(pady=5, padx=5, row=0, column=0)
    
    frDatosNuevoComprador = Frame(frNuevoComprador, bg="#ccedf8")
    frDatosNuevoComprador.grid(pady=5, padx=5, row=0, column=0)
    
    Label(frDatosNuevoComprador, text="Numero de Identificacion").grid(pady=5, padx=5, row=0, column=0)
    self.in_TxtCodigoNuevoComprador=Entry(frDatosNuevoComprador, width=30)
    self.in_TxtCodigoNuevoComprador.grid(padx=5, pady=5, row=0, column=1)
    self.in_TxtCodigoNuevoComprador.focus()
    self.in_TxtCodigoNuevoComprador.bind("<Return>", self.fEnterCodigoNuevoComprador)
    
    Label(frDatosNuevoComprador, text="Nombre").grid(pady=5, padx=5, row=1, column=0)
    self.in_TxtNombreNuevoComprador=Entry(frDatosNuevoComprador, width=30, state="disabled")
    self.in_TxtNombreNuevoComprador.grid(padx=5, pady=5, row=1, column=1)
    self.in_TxtNombreNuevoComprador.bind("<Return>", self.fEnterNombreNuevoComprador)
    
    Label(frDatosNuevoComprador, text="Apellido").grid(pady=5, padx=5, row=2, column=0)
    self.in_TxtApellidoNuevoComprador=Entry(frDatosNuevoComprador, width=30, state="disabled")
    self.in_TxtApellidoNuevoComprador.grid(padx=5, pady=5, row=2, column=1)
    self.in_TxtApellidoNuevoComprador.bind("<Return>", self.fEnterApellidoNuevoComprador)
    
    Label(frDatosNuevoComprador, text="Contratista").grid(pady=5, padx=5, row=3, column=0)
    self.in_TxtContratistaNuevoComprador=Entry(frDatosNuevoComprador, width=30, state="disabled")
    self.in_TxtContratistaNuevoComprador.grid(padx=5, pady=5, row=3, column=1)
    self.in_TxtContratistaNuevoComprador.bind("<Return>", self.fEnterContratistaNuevoComprador)
    
    frBtnGuardarNuevoComprador = Frame(frNuevoComprador, bg="#C1FFBE")
    frBtnGuardarNuevoComprador.grid(padx=5, pady=5,row=1, column=0)
    
    self.btnGuardarNuevoComprador=Button(frBtnGuardarNuevoComprador, text="Guardar", command=self.funBtnGuardarNuevoComprador, bg="#f87c7c", fg="#ffffff", state="disabled")
    self.btnGuardarNuevoComprador.grid(padx=5, pady=5,row=4, column=0)
    
    self.btnCancelarNuevoComprador=Button(frBtnGuardarNuevoComprador, text="Cancelar", command=self.funBtnCancelarNuevoComprador, bg="#f87c7c", fg="#ffffff")
    self.btnCancelarNuevoComprador.grid(padx=5, pady=5,row=4, column=1)