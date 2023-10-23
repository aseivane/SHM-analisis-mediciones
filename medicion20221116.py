from Medicion import Medicion


if __name__ == '__main__':
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20221116-073/'
    limiteInf = 1000
    limiteSup = 1200

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1)
    medicion.quitarMediaAceleracion()
    medicion.cambiarEscalaAceleracion(escalaAceleracion)
    
    medicion.correlacionConImpulso()

    medicion.graficarCorrelacion()
    medicion.graficarTemporal(limiteInf,limiteSup)