from Medicion import Medicion
import numpy as np


if __name__ == '__main__':
    x_limiteInf = 449300/30000
    x_limiteSup = 449500/30000
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20230719-015/'

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1,"nodo_94b97eda9150")
    medicion.quitarMediaAceleracion()
    medicion.cambiarEscalaAceleracion(escalaAceleracion)
    
    medicion.correlacionConImpulso()

    medicion.graficarCorrelacion()
   
    axinsUbicacion = [0.05, 0.05, 0.6, 0.4]
    axinsKargs = {"xlim": (x_limiteInf, x_limiteSup),
            "xticklabels": [], 
            "yticklabels": []}
    medicion.graficarTemporal(axinsUbicacion, axinsKargs)