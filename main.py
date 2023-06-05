from tkinter import *
from ventana import *
from reporte import *
from tkinter import ttk
#Hola
def main():
  root=Tk() 
  
  panel = ttk.Notebook(root)
  panel.pack(fill="both", expand=YES)
  
  tab1 = ttk.Frame(panel)
  panel.add(tab1, text="Ventas")
  
  tab2 = ttk.Frame(panel)
  panel.add(tab2, text="Reportes")
  
  root.wm_title("Aplicacion Agro Servicios JL SAS")
  app1=Ventana(tab1)
  app2=Reporte(tab2)
  app1.mainloop()
  app2.mainloop()
    
if __name__=="__main__":
  main()