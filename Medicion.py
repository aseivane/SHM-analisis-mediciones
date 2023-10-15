from Nodo import Nodo
import os
import matplotlib.pyplot as plt



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
        fig, ( ax_nodos, ax_corr, ax_lag) = plt.subplots(3, 1)
        
        ax_nodos.set_title('Nodos')
        for nodo in self.listaNodos: 
            ax_nodos.plot(nodo.accelerationY, label= nodo.nodo)
            for key in nodo.correlaciones.keys():
                ax_corr.plot(nodo.correlaciones[key].matrizCorrelacion, 
                             label=nodo.nodo+'-'+key)

        ax_nodos.legend()
        ax_corr.legend()
        ax_corr.set_title('Correlacion')
        #for correlacion in self.matrizCorrelacion:
        #    ax_corr.plot(correlacion)

        '''
        lagsNodo_34ab958660d0, corrNodo_34ab958660d0, 'b-')
        ax_corr.plot(lagsNodo_34ab958660d0[localMaxsNodo_34ab958660d0], corrNodo_34ab958660d0[localMaxsNodo_34ab958660d0], 'ro')

        ax_corr.plot(lagsNodo_94b97eda9150, corrNodo_94b97eda9150, 'g-')
        ax_corr.plot(lagsNodo_94b97eda9150[localMaxsNodo_94b97eda9150], corrNodo_94b97eda9150[localMaxsNodo_94b97eda9150], 'yo')


        ax_corr.plot(lagsNodo_94b97eda2f1c, corrNodo_94b97eda2f1c, 'k-')
        ax_corr.plot(lagsNodo_94b97eda2f1c[localMaxsNodo_94b97eda2f1c], corrNodo_94b97eda2f1c[localMaxsNodo_94b97eda2f1c], 'wo')

        ax_corr.set_title('Correlacion cruzada con impulso')
        ax_corr.set_xlabel('Lag')

        
        '''
        fig.tight_layout()
        plt.show()
