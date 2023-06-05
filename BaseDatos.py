import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from tkinter import ttk, messagebox
import time
from datetime import datetime

class BaseDatos:
  
  def __init__(self):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
                  "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("D:/Documentos/RADA/Aplicacion Agro Servicios JL SAS/agroserviciosjl-credencial.json", scope)
    self.client=gspread.authorize(creds)
    
    self.sheet = self.client.open("PrimeraBase")
    #self.worksheetProductos = self.sheet.worksheet("Productos")
    #self.worksheetCompradores = self.sheet.worksheet("Compradores")
    #self.worksheetVentas = self.sheet.worksheet("Ventas")
     
  def __str__(self):
    pass    
    
  def fObtenerCodigo(self, nameWorksheet):
    worksheet = self.sheet.worksheet(nameWorksheet)
    dataCod = worksheet.col_values(1)
    return dataCod
  
  def fObtenerContratista(self, nameWorksheet):
    worksheet = self.sheet.worksheet(nameWorksheet)
    Contratistas = worksheet.col_values(4)
    auxContratista = []
    [auxContratista.append(cntra) for cntra in Contratistas if cntra not in auxContratista]
    return auxContratista
  
  def fObtenerDatos(self, nameWorksheet, codigo):
    worksheet = self.sheet.worksheet(nameWorksheet)
    data = worksheet.find(codigo)
    data = worksheet.get_values('A{0}:D{0}'.format(data.row))[0]
    return data
  
  def fBuscarDatos(self, nameWorksheet, codigo):
    worksheet = self.sheet.worksheet(nameWorksheet)
    data = worksheet.get_all_values()
    index = 0
    auxLista = []
    for listData in data:
      match = [s for s in listData if codigo in s]
      if match:
        lista = data[index]
        #lista = worksheet.find(match[0])
        #lista = worksheet.get_values('A{0}:D{0}'.format(lista.row))[0]
        auxLista.append(lista)
      index +=1
    time.sleep(5)
    return auxLista
  
  def fBuscarReportes(self, nameWorksheet, codigo, fechaInicio, fechaFinal):
    worksheet = self.sheet.worksheet(nameWorksheet)
    data = worksheet.get_all_values()
    index = 0
    auxLista = []
    fechaInicio = datetime.strptime(str(fechaInicio), "%Y-%m-%d")
    fechaFinal = datetime.strptime(str(fechaFinal), "%Y-%m-%d")
    for listData in data:
      match = [s for s in listData if codigo in s]
      if match:
        lista = data[index]
        if nameWorksheet == "Ventas":
          fecha = lista[8].split(" ")
          fecha = datetime.strptime(fecha[0], "%Y-%m-%d")
          if fecha >= fechaInicio and fecha <= fechaFinal:
            auxLista.append(lista)
      index +=1
    return auxLista
  
  def fAgregarDatos(self, nameWorksheet, listDatos):
    worksheet = self.sheet.worksheet(nameWorksheet)
    numFila = worksheet.col_values(1)
    if (nameWorksheet == "Compradores") and (str(listDatos[0]) in numFila):
      messagebox.showerror(
      title="Error Registro",
      message="El Registro ya existe verifica el numero de identificacion"
      )
    else:
      column=1
      for dato in listDatos:
        worksheet.update_cell(len(numFila)+1, column, dato)
        column+=1
        time.sleep(1)
        
  def fDescontarCantidad(self, nameWorksheet, codigoVenta, cantidadVenta):
    worksheet = self.sheet.worksheet(nameWorksheet)
    cod = worksheet.col_values(1)
    index = cod.index(str(codigoVenta))
    ctd = worksheet.cell(index+1, 4).value
    ctd = int(ctd) - int(cantidadVenta)
    worksheet.update_cell(index+1, 4, ctd)
    time.sleep(5)
      
