import requests
import json
import time
import glob
import os

from tkinter import *
from tkinter import Frame
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from pathlib import Path
import pickle
from tkinter import ttk
import math
from datetime import datetime


class Dia():
    def __init__(self, tempmax, tempmin,climadia,climanoche,fecha,icond,iconn):
        self.tmax = tempmax
        self.tmin = tempmin
        self.cd = climadia
        self.cn = climanoche
        self.fecha = fecha #id
        self.icd=icond
        self.icn=iconn

class Lista_Dias():
    dias=[]
    def __init__(self):
        
        try:
            listaD=open("Dias","ab+")
            
        except:
            
            print(" No se creo archivo")
        listaD.seek(0)
        try:
            
            self.dias=pickle.load(listaD)
        except:
            print("Archivo vacio,no se puede modificar ni eliminar datos")
        finally:
            listaD.close()
            del(listaD)

    def insertar_dias(self,dias):
        for dn in dias:
            if self.buscar_dia(dn.fecha)>=0:
                
                self.modificar_dia(dn,self.buscar_dia(dn.fecha))
                continue

            else:
                self.dias.append(dn)

        self.dias_a_fichero()

    def dias_a_fichero(self):
        listaD=open("Dias","wb")
        pickle.dump(self.dias,listaD)
        listaD.close()
        del(listaD)
    
    def mostrar_dias(self):
        for d in self.dias:
            print("\n")
            print(d.fecha)
            print(d.tmax)
    
    def buscar_dia(self,dn):
        
        for d in self.dias:
            if d.fecha==dn:
                print(d.fecha)
                print(self.dias.index(d))
                return self.dias.index(d)
                break
            
        return -1
    '''
    def estadisticas_dia(self):
        for e in self.dias:
            pass
    '''        
    
    def modificar_dia(self,dn,i):
        print("modificar dia:" + self.dias[i].fecha +" a "+ dn.fecha)
        self.dias[i].tmax=dn.tmax
        self.dias[i].tmin=dn.tmin
        self.dias[i].cd=dn.cd
        self.dias[i].cn=dn.cn
        self.dias[i].icd=dn.icd
        self.dias[i].icn=dn.icn        
        self.dias_a_fichero()

    def obtener_info_dias(self,fi,ff):
        lista_estadistica=[]
        for dia in self.dias:
            date_object = datetime.strptime(dia.fecha, '%Y-%m-%d')
            if date_object>=fi and date_object<=ff:
                lista_estadistica.append(dia)
        return lista_estadistica

    
        




listadedias=Lista_Dias()

def crear_ventana():
    listadedias.mostrar_dias()
    global ventana
    ventana =Tk()
    #ventana.configure()
    #ventana.geometry("1000x1000")
    ventana.resizable(False,False)
    ventana.title("Clima")

    global miFrame
    
    miFrame=Frame(ventana,width=1000,height=600)
        
    miFrame.config(bg='light blue')
    #miFrame.grid_propagate(False)
    miFrame.pack(fill="x")
    
    
    crear_boton_guardar(miFrame)
    crear_boton_mostrar(miFrame)
    crear_boton_salir(miFrame)
    crear_boton_analisis(miFrame)

    ventana.mainloop()
#botones form 1
def crear_boton_guardar(miFrame):
    boton1 = Button(miFrame, text="guardar datos", command=lambda: guardar_datos(consumir_datos()))
    boton1.grid(column=0,row=0,padx=5)

def crear_boton_mostrar(miFrame):
    boton2 = Button(miFrame, text="mostrar clima", command= lambda: crear_dias_clima(consumir_datos()))
    boton2.grid(column=1,row=0,padx=5)

def crear_boton_salir(miFrame):
    boton3 = Button(miFrame, text="salir", command=finalizar)
    boton3.grid(column=2,row=0,padx=5)

def crear_boton_analisis(miFrame):
    boton4 = Button(miFrame, text="analisis", command=crear_form2)
    boton4.grid(column=3,row=0,padx=5)

#accion botones primer form
def consumir_datos():
    url='http://dataservice.accuweather.com/forecasts/v1/daily/5day/52485?apikey=qewmMTemizqPCWPAohpOBN912y8ALtEB&language=es-cl&metric=true'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        content = response.json()
        #print(content['DailyForecasts'][0]['Date'])
    lista=[]
    for a in range(0,5):
    # lista.append(content['DailyForecasts']['0'])
    #return lista
        fecha = content['DailyForecasts'][a]['Date']
        fecha = crear_fecha(fecha)
        
        tmax = content['DailyForecasts'][a]['Temperature']['Minimum']['Value']
        tmin = content['DailyForecasts'][a]['Temperature']['Maximum']['Value']
        cd = content['DailyForecasts'][a]['Day']['IconPhrase']
        icond = content['DailyForecasts'][a]['Day']['Icon']
        cn = content['DailyForecasts'][a]['Night']['IconPhrase']
        iconn = content['DailyForecasts'][a]['Night']['Icon']
        lista.append(Dia(tmax,tmin,cd,cn,fecha,icond,iconn))
    return lista


def crear_fecha(stringf):
    stringf = stringf.split("T",1)
    stringf = stringf[0]
    return stringf

def mostrar_datos(lista):
    for obj in lista:
        print(obj.fecha)
        
def crear_dias_clima(lista):
    frames=[]
    #l = len(lista)
    #width = miFrame.winfo_reqwidth()
    #prop = (width/l)/width
    global framedatos
    framedatos=Frame(ventana)
    framedatos.pack(anchor="s")

    index=0
    for obj in lista:
        
        frames.append(crear_frame(obj,index))
        frames[index].grid(column=index,row=0)
        index=index+1

def crear_frame(obj,i):
    f=Frame(framedatos)
    #backOne = os.path.dirname(cwd)
    #print(backOne)
    #cwd = os.getcwd()
    #print(cwd)
    
    
    #data_folder = Path(cwd)
    #file_to_open = data_folder / nombre_imagen
    
    #print(file_to_open)
    
    lblfecha=Label(f,text=obj.fecha)
    lblfecha.pack()

    lbltmin=Label(f,text="T° minima: "+str(obj.tmin))
    lbltmin.pack()

    lbltmax=Label(f,text="T° maxima: "+str(obj.tmax))
    lbltmax.pack()
    
    lblclimad=Label(f,text=obj.cd)
    lblclimad.pack()

    v= obj.icd #codigo del icono
    url="https://developer.accuweather.com/sites/default/files/"+str(v)+"-s.png"
    response1 = requests.get(url, stream=True)
    with open('iconodia'+str(i)+'.png','wb') as icd:
        for chunk in response1.iter_content():
            icd.write(chunk)
    response1.close()
   
    nombre_imagen="iconodia"+str(i)+".png"
    try: 
        imagen= Image.open(nombre_imagen)
        imagen_label = ImageTk.PhotoImage(imagen)
    
        lblicd=Label(f,image=imagen_label)
        lblicd.image =imagen_label
        lblicd.pack()
    except:
        lblicd=Label(f,text="""No se pudo
        cargar la imagen""")
        lblicd.pack()

    lblcliman=Label(f,text=obj.cn)
    lblcliman.pack()

    v= obj.icn
    url="https://developer.accuweather.com/sites/default/files/"+str(v)+"-s.png"
    response1 = requests.get(url, stream=True)
    with open('icononoche'+str(i)+'.png','wb') as icn:
        for chunk in response1.iter_content():
            icn.write(chunk)
    response1.close()
    
    nombre_imagen="icononoche"+str(i)+".png"
    try:
        imagen= Image.open(nombre_imagen)
        imagen_label = ImageTk.PhotoImage(imagen)
    
        lblicn=Label(f,image=imagen_label)
        lblicn.image =imagen_label
        lblicn.pack()
    except:
        lblicn=Label(f,text="""No se pudo
        cargar la imagen""")
        
        lblicn.pack()

    return f



def guardar_datos(lista):
    listadedias.insertar_dias(lista)

def finalizar():
    for i in range(0,5):
        if os.path.isfile("iconodia"+str(i)+".png"):
            os.remove("iconodia"+str(i)+".png") 
            os.remove("icononoche"+str(i)+".png") 
    exit()

def crear_form2():
    global ventana2
    ventana2 =Tk()
    
    ventana2.geometry("1000x500")
    ventana2.resizable(False,False)
    ventana2.title("Analisis Clima")

    global miFrame2
    
    miFrame2=Frame(ventana2,width="1000",height="500")
    
        
    
    miFrame2.pack()
    #miFrame2.grid_propagate(False)
    global lblinicio
    lblinicio = Label(miFrame2,text="Fecha Inicio(%Y/%mm/%dd)")
    lblinicio.grid(row=0, column=0)
    global tbinicio
    tbinicio=ttk.Entry(miFrame2)
    tbinicio.grid(row=0, column=1)

    global lblfinal
    lblfinal = Label(miFrame2,text="Fecha final(%Y/%mm/%dd)")
    lblfinal.grid(row=1, column=0)
    global tbfinal
    tbfinal=ttk.Entry(miFrame2)
    tbfinal.grid(row=1, column=1)

    

    boton21 = Button(miFrame2, text="Ver Estadisticas", command=analisis)
    boton21.grid(column=0,row=2,padx=5,columnspan=2)

    ventana2.mainloop()



def analisis():
    
     
    fi = datetime.strptime(tbinicio.get(), '%Y-%m-%d')
    ff = datetime.strptime(tbfinal.get(), '%Y-%m-%d')
    if fi<=ff:
        pass
    else:
        exit()  
            
    
    lbl1 = Label(miFrame2,text="Maximo: "+str(maximo(listadedias.obtener_info_dias(fi,ff))))
    lbl1.grid(row=3, column=0)
    
    lbl2 = Label(miFrame2,text="Minimo: "+str(minimo(listadedias.obtener_info_dias(fi,ff))))
    lbl2.grid(row=4, column=0)
    
    lbl3 = Label(miFrame2,text="Promedio: "+str(promedio(listadedias.obtener_info_dias(fi,ff))))
    lbl3.grid(row=5, column=0)
    
    dic = porcentajed(listadedias.obtener_info_dias(fi,ff))
    dic2= porcentajen(listadedias.obtener_info_dias(fi,ff))

    ac=0
    for d in dic:
        ac=ac+d

    lbl41 = Label(miFrame2,text="Porcentaje Dia: ")
    lbl41.grid(row=6, column=0)
    n=7
    for k,v in porcentajed(listadedias.obtener_info_dias(fi,ff)).items():

        l=Label(miFrame2,text=k+": ")
        l.grid(row=n,column=0)

        l=Label(miFrame2,text=k+": ")
        l.grid(row=n,column=1)
        n=n+1


    print(dic)
    print(dic2)
    '''
    for d in dic:
        lbl4=Label(miFrame2,text=)
    '''
def entero(v):
    try:
        int(v)
        return True
    except:
        return False

def minimo(lista):
        minimo=500
        for dia in lista:
            numero=float(dia.tmin)

            if(numero<minimo):

                minimo=numero
        return numero

def maximo(lista):
    maximo=-100
    for dia in lista:
        numero=float(dia.tmax)

        if(numero>maximo):

            maximo=numero
    return numero

def promedio(lista):
    #maximo=-100
    acum=0
    index=0
    for dia in lista:
        max=float(dia.tmax)
        min=float(dia.tmin)
        index=index+2
        acum=acum+max+min

    prom=acum/index
    return prom

def porcentajed(lista):
    dic={}
    
    for dia in lista:
        v=dia.cd
        try:
            if dic[v] != None:
                dic[v]=dic.get(v)+1
            
        except:
            dic.setdefault(v,1)
    return dic

def porcentajen(lista):
    
    dic2={}
    for dia in lista:
        
        d=dia.cn
        try:
            if dic2[d]!= None:
                dic2[d]=dic2.get(d)+1
            
        except:
            dic2.setdefault(d,1)
    return dic2
#main
#mostrar_datos(consumir_datos())

crear_ventana()

#ventana.mainloop()