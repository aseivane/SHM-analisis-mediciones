from Nodo import Nodo
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta




class Medicion:
    def __init__(self, dirName) -> None:
        # archivo de un minuto con 500 mustras por segundo
        self.muestrasPorArchivo = 30000 
        #si no existe el directorio, sale
        if not os.path.exists(dirName):
            print("ERROR: No existe el directorio")
            exit()

        #define los atributos basicos de la Medicion
        self.separator='/'#'\\'
        self.carpetaMedicion = dirName
        if self.carpetaMedicion[-1] == self.separator:
            self.carpetaMedicion = self.carpetaMedicion[:-1] #remove trailing slash

        dirObjects = dirName.split(self.separator)

        self.nombreMedicion = dirObjects[-1]

        self.listaNodos = []

        self.agregarNodos()

        self.cantNodos = len(self.listaNodos)

        self.largoMedicion = self.cantidadArchivos() * self.muestrasPorArchivo

        if self.largoMedicion <= self.muestrasPorArchivo :
            self.arrayTiempo = np.arange(0, self.largoMedicion/self.muestrasPorArchivo + 0.5, 0.5)
        elif (self.largoMedicion / self.muestrasPorArchivo) <= 10 :
            self.arrayTiempo = np.arange(0, self.largoMedicion/self.muestrasPorArchivo + 1, 1)
        else :
            self.arrayTiempo = np.arange(0, self.largoMedicion/self.muestrasPorArchivo + 2, 2)
        #self.arrayTiempo = self.arrayTiempo / self.largoMedicion
       # print(self.arrayTiempo)

        
    def agregarNodos(self) -> None:
        listaCarpetaNodos = next(os.walk(self.carpetaMedicion))[1]

        for carpetaNodo in listaCarpetaNodos:
            direccionNodo = os.path.join(self.carpetaMedicion, carpetaNodo)
            self.listaNodos.append(Nodo(direccionNodo))

    def cantidadArchivos(self) -> int:
        
        cantidad = 0
        indice = 0
        # Iterate directory
        dirList = os.listdir(self.carpetaMedicion)
        nodo1 = os.path.join(self.carpetaMedicion, dirList[0])
        while os.path.isfile(nodo1) and indice < len(dirList):
            indice += 1
            nodo1 = os.path.join(self.carpetaMedicion, dirList[indice])


        dirList = os.listdir(nodo1)
        for archivo in dirList:
            # check if current path is a file
            if os.path.isfile(os.path.join(nodo1, archivo)):
                cantidad += 1
        return cantidad
    
    def cambiarEscalaAceleracion(self, escala, nodo = "all") -> None:
        for index in range(self.cantNodos):
            self.listaNodos[index].cambiarEscalaAcelerometro(escala, nodo)
                           
    def quitarMediaAceleracion(self) -> None:
        for index in range(self.cantNodos):
            self.listaNodos[index].quitarMediaAceleracion()

    def correlacionConImpulso(self):
        
        impulso = []
        for index in range(self.cantNodos):
            self.listaNodos[index].crearCorrelacion(impulso, "impulso")
            
    def graficarCorrelacion(self):
        def histograma(axHist):
            axHist.set_title('Histograma')
            listaDeltas = []
            matrixDeltas = [] 
            for index in range(self.cantNodos):
                nodo = self.listaNodos[index]
                for key in nodo.correlaciones.keys():
                    matrixDeltas.insert(index, nodo.correlaciones[key].localMaxs)

            for nodo1 in range(self.cantNodos):
                for nodo2 in range(self.cantNodos):
                    if nodo1 != nodo2:
                        diferenciaLags = matrixDeltas[nodo1] - matrixDeltas[nodo2]
                        listaDeltas.append( diferenciaLags)

            listaDeltas = np.array(listaDeltas)
            listaDeltas = listaDeltas[listaDeltas >= 0]
            axHist.hist(listaDeltas)
            axHist.set_xticks([0, 1, 2, 3])
            axHist.set_xlabel("Distancia entre muestras")
            axHist.grid(True)

        def graficoTemporal(ax_nodos, ax_lag):
            ax_nodos.set_title('Temporal')
            ax_lag.set_title('Correlacion')

            for nodo in self.listaNodos: 
                tiempo_en_minutos = np.arange(len(nodo.accelerationX)) / 500 / 60.0 

                ax_nodos.plot(tiempo_en_minutos, nodo.accelerationX, label= nodo.nodo)
                for key in nodo.correlaciones.keys():

                    correlacionActual = nodo.correlaciones[key]
                    
                    ax_lag.plot( correlacionActual.lags/ 500 / 60.0 , 
                                correlacionActual.correlacion,
                                label=nodo.nodo+'-'+key)
                    
                    ax_lag.plot( correlacionActual.lags[correlacionActual.localMaxs]/ 500 / 60.0 ,
                                correlacionActual.correlacion[correlacionActual.localMaxs], 'o')


            ax_nodos.legend(loc='upper right')
            ax_nodos.set_ylabel("Aceleración [m/s^2]")
            ax_lag.legend(loc='lower right')
            ax_lag.set_xlabel("Tiempo [min]")
            xlabels = [f'{x:}' for x in self.arrayTiempo]
            ax_lag.set_xticks(self.arrayTiempo, labels=xlabels)
            ax_lag.grid(True)

        fig, ( ax_nodos, ax_lag) = plt.subplots(2, 1, figsize =(8, 6),sharex=True)
        #fig.tight_layout()

        graficoTemporal(ax_nodos, ax_lag)

        histFig, axHist = plt.subplots(figsize =(3, 5))
        histograma(axHist)
  
        plt.show()

    def graficarTemporal(self, axinsUbicacion, axinsKargs):

        fig, ( ax_t) = plt.subplots(figsize=[8,6])
        ax_t.set_title('Respuesta temporal')

        
        axins = ax_t.inset_axes(axinsUbicacion, **axinsKargs )
        
        axins.grid(True)

        ax_t.set_ylim(bottom=-30,top = 50)


        for nodo in self.listaNodos: 
            tiempo_en_minutos = np.arange(len(nodo.accelerationX)) / 500 / 60.0

            ax_t.plot( tiempo_en_minutos, nodo.accelerationX, label= nodo.nodo)
            axins.plot( tiempo_en_minutos, nodo.accelerationX)

        ax_t.indicate_inset_zoom(axins, edgecolor="black")

        ax_t.legend(loc='upper left')
        ax_t.set_xlabel("Tiempo [min]")
        ax_t.set_ylabel("Aceleración [m/s^2]")
        xlabels = [f'{x:}' for x in self.arrayTiempo]
        ax_t.set_xticks(self.arrayTiempo, labels=xlabels)

        plt.show()
