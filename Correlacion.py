from scipy import signal
import numpy as np

class Correlacion:
    def __init__(self,señal1, señal2) -> None:
        self.Correlacion = []
        self.Lags = []
        
        self.correlacion = signal.correlate( señal1, señal2 )
        self.correlacion /= np.max(self.correlacion)

        self.lags = signal.correlation_lags( len(señal1), len(señal2) )

        self.localMaxs, _ = signal.find_peaks(self.correlacion, height=0.8)
        self.localMaxsDist = np.diff(self.localMaxs)
        


    
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