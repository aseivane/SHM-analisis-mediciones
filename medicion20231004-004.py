from Medicion import Medicion


if __name__ == '__main__':
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20231004-004/'
    x_limiteInf = 10000/30000
    x_limiteSup = 12000/30000

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1,"nodo_34ab958660d0_")
    medicion.quitarMediaAceleracion()
    #medicion.cambiarEscalaAceleracion(escalaAceleracion)
    
    #medicion.correlacionConImpulso()

    #medicion.graficarCorrelacion()
    axinsUbicacion = [0.05, 0.05, 0.6, 0.4]
    axinsKargs = {"xlim": (x_limiteInf, x_limiteSup),
            "xticklabels": [], 
            "yticklabels": []}
    medicion.graficarTemporal(axinsUbicacion, axinsKargs)