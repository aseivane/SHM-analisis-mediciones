from Nodo import Nodo
import os
import matplotlib.pyplot as plt
import numpy as np



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
        
    def agregarNodos(self) -> None:
        listaCarpetaNodos = next(os.walk(self.carpetaMedicion))[1]

        for carpetaNodo in listaCarpetaNodos:
            direccionNodo = os.path.join(self.carpetaMedicion, carpetaNodo)
            self.listaNodos.append(Nodo(direccionNodo))

    def cantidadArchivos(self) -> int:
        
        cantidad = 0
        # Iterate directory
        dirList = os.listdir(self.carpetaMedicion)
        nodo1 = os.path.join(self.carpetaMedicion, dirList[0])
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
            axHist.hist(listaDeltas,bins=[0, 1, 2, 3])

        def graficoTemporal(ax_nodos, ax_corr, ax_lag):
            ax_nodos.set_title('Nodos')
            ax_corr.set_title('Correlacion')
            ax_lag.set_title('Lag')

            for nodo in self.listaNodos: 
                ax_nodos.plot(nodo.accelerationX, label= nodo.nodo)
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

        fig, ( ax_nodos, ax_corr, ax_lag) = plt.subplots(3, 1, sharex=True)
        fig.tight_layout()

        graficoTemporal(ax_nodos, ax_corr, ax_lag)

        histFig, axHist = plt.subplots(figsize =(8, 6))
        histograma(axHist)
  
        plt.show()

    def graficarTemporal(self,limiteInf, limiteSup):
        #from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
        #from mpl_toolkits.axes_grid1.inset_locator import mark_inset
        def referenciaMuyChica() -> bool:
            anchoRectangulo = limiteSup - limiteInf
            anchoMinimo = 0.5 * self.largoMedicion
            print(anchoMinimo)

            if anchoRectangulo < anchoMinimo:
                return True
            
            return False

        fig, ( ax_t) = plt.subplots(figsize=[8,6])
        ax_t.set_title('Respuesta temporal')
        #axins = zoomed_inset_axes([10000, 4, 15000, 8], 6) # zoom = 6
        
        #if referenciaMuyChica():
        #    limiteSup = limiteInf + 0.1 * self.largoMedicion

        axins = ax_t.inset_axes(
            [0.52, 0.55, 0.6, 0.4],
            xlim=(limiteInf, limiteSup), xticklabels=[], yticklabels=[])
        
        axins.grid(True)

        ax_t.set_ylim(bottom=-30,top = 50)


        for nodo in self.listaNodos: 
            ax_t.plot(nodo.accelerationX, label= nodo.nodo)
            axins.plot(nodo.accelerationX)

        ax_t.indicate_inset_zoom(axins, edgecolor="black")

        ax_t.legend(loc='upper left')

        plt.show()
