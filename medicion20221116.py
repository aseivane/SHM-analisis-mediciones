from Medicion import Medicion


if __name__ == '__main__':
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20221116-073/'
    x_limiteInf = 29000/30000
    x_limiteSup = 29100/30000

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1)
    medicion.quitarMediaAceleracion()
    medicion.cambiarEscalaAceleracion(escalaAceleracion)
    
    medicion.correlacionConImpulso()

    medicion.graficarCorrelacion()
    axinsUbicacion = [0.05, 0.05, 0.6, 0.4]
    axinsKargs = {"xlim": (x_limiteInf, x_limiteSup),
            "xticklabels": [], 
            "yticklabels": []}
    medicion.graficarTemporal(axinsUbicacion, axinsKargs)