from scipy import signal
import numpy as np

class Correlacion:
    def __init__(self,señal1, señal2) -> None:
        self.matrizCorrelacion = []
        self.matrizLags = []
        
        self.matrizCorrelacion = signal.correlate( señal1, señal2 )
        self.matrizCorrelacion /= np.max(self.matrizCorrelacion)

        self.matrizLags = signal.correlation_lags( len(señal1), len(señal2) )
        

    def correlacionConImpulso(self, largo, ordenFiltro, wc):
        def correlacionNodoImpulso():
            #self.correlacionCon = 'impulso'
            self.matrizCorrelacion = [ signal.correlate( nodo.accelerationY, self.impulso ) for nodo in self.medicion.listaNodos ]
            self.matrizCorrelacion = [ corr/np.max(corr) for corr in self.matrizCorrelacion ] 

            self.matrizLags = [ signal.correlation_lags( len(nodo.accelerationY), len(self.impulso) ) for nodo in self.medicion.listaNodos ]
        

        

        self.impulso = self.crearImpulsoFiltrado(largo, ordenFiltro, wc)

        correlacionNodoImpulso()

        
        graficoCorrelacionImpulso()
        

    def crearImpulsoFiltrado(self, largo, ordenFiltro, wc ):
        imp = signal.unit_impulse(largo)
        b, a = signal.butter(ordenFiltro, wc)
        return signal.lfilter(b, a, imp)


    
'''
# Convert the list to a NumPy array
nodo_94b97eda2f1c = np.array(second_column_values)*-1

nodo_94b97eda2f1c = (nodo_94b97eda2f1c - np.mean(nodo_94b97eda2f1c))/16384
nodo_94b97eda2f1c = nodo_94b97eda2f1c * 9.806
nodo_94b97eda2f1cCortado = nodo_94b97eda2f1c[:anchoVentana]

corrNodo_94b97eda2f1c= signal.correlate(nodo_94b97eda2f1cCortado, impulseResponse)
lagsNodo_94b97eda2f1c = signal.correlation_lags(len(nodo_94b97eda2f1cCortado), len(impulseResponse))
corrNodo_94b97eda2f1c /= np.max(corrNodo_94b97eda2f1c)

localMaxsNodo_94b97eda2f1c, _ = signal.find_peaks(corrNodo_94b97eda2f1c, height=0.8)
localMaxsDistNodo_94b97eda2f1c = np.diff(localMaxsNodo_94b97eda2f1c)

'''