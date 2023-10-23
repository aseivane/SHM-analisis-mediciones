from Medicion import Medicion


if __name__ == '__main__':

    limiteInf = 0
    limiteSup = 300
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20230719-015/'

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1,"nodo_94b97eda9150")
    medicion.quitarMediaAceleracion()
    medicion.cambiarEscalaAceleracion(escalaAceleracion)
    
    medicion.correlacionConImpulso()

    medicion.graficarCorrelacion()
    medicion.graficarTemporal(limiteInf,limiteSup)