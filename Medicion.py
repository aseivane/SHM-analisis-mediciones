from Nodo import Nodo
import os
import matplotlib.pyplot as plt
import numpy as np



class Medicion:
    def __init__(self, dirName) -> None:
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
        
    def agregarNodos(self) -> None:
        listaCarpetaNodos = next(os.walk(self.carpetaMedicion))[1]

        for carpetaNodo in listaCarpetaNodos:
            direccionNodo = os.path.join(self.carpetaMedicion, carpetaNodo)
            self.listaNodos.append(Nodo(direccionNodo))

    def cantidadArchivos(self) -> int:
        
        cantidad = 0
        # Iterate directory
        for archivo in self.dirName:
            # check if current path is a file
            if os.path.isfile(os.path.join(self.dirName, archivo)):
                cantidad += 1
        return cantidad
    
    def cambiarEscalaAceleracion(self, escala, nodo = "all") -> None:
        for index in range(self.cantNodos):
            self.listaNodos[index].cambiarEscalaAcelerometro(escala, nodo)
                           
    
    def quitarMediaAceleracion(self) -> None:
        for index in range(self.cantNodos):
            self.listaNodos[index].quitarMediaAceleracion()

    def correlacionConImpulso(self, largo, ordenFiltro, wc):
        # def crearImpulso(largo, ordenFiltro, wc ):
        #     imp = signal.unit_impulse(largo)
        #     b, a = signal.butter(ordenFiltro, wc)
        #     return signal.lfilter(b, a, imp)

        # impulso = crearImpulso(largo, ordenFiltro, wc)
        impulso = []
        for index in range(self.cantNodos):
            self.listaNodos[index].crearCorrelacion(impulso, "impulso")
            
    def graficarCorrelacion(self):
        fig, ( ax_nodos, ax_corr, ax_lag) = plt.subplots(3, 1, sharex=True)
        
        ax_nodos.set_title('Nodos')
        ax_corr.set_title('Correlacion')
        ax_lag.set_title('Lag')

        for nodo in self.listaNodos: 
            ax_nodos.plot(nodo.accelerationY, label= nodo.nodo)
            for key in nodo.correlaciones.keys():

                correlacionActual = nodo.correlaciones[key]

                ax_corr.plot(correlacionActual.correlacion, 
                             label=nodo.nodo+'-'+key)
                
                ax_lag.plot(correlacionActual.lags, 
                            correlacionActual.correlacion,
                             label=nodo.nodo+'-'+key)
                
                ax_lag.plot(correlacionActual.lags[correlacionActual.localMaxs],
                             correlacionActual.correlacion[correlacionActual.localMaxs], 'o')


        ax_nodos.legend()
        ax_corr.legend()
        ax_lag.legend()
        fig.tight_layout()

        histFig, axHist = plt.subplots(figsize =(10, 7))
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
        axHist.hist(listaDeltas,bins=[0, 1, 2, 3])
  
        plt.show()
