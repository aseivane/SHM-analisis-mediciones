from Medicion import Medicion
import numpy as np


if __name__ == '__main__':
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20231004-002/'
    x_limiteInf = 8.999#100000/30000
    x_limiteSup = 9.001#100100/30000

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1,"nodo_34ab958660d0_")
    medicion.quitarMediaAceleracion()
    medicion.cambiarEscalaAceleracion(escalaAceleracion)

    y_limiteSup = 0.5
    y_limiteInf = -0.3
    axinsKargs = {  "xlim": (x_limiteInf, x_limiteSup),
                    "ylim": (y_limiteInf, y_limiteSup),
                    "xticklabels": [], 
                    "yticklabels": []}
    axinsUbicacion = [0.5, 0.5, 0.6, 0.4]
    
    #medicion.correlacionConImpulso()

    #medicion.graficarCorrelacion()
    medicion.graficarTemporal(axinsUbicacion, axinsKargs)