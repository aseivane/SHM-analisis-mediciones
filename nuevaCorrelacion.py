from Medicion import Medicion


if __name__ == '__main__':
    largo = 125
    ordenFiltro = 4
    wc = 6/largo
    #directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20221116-073/'
    directory = '/Users/aseivane/Documents/SHM/SHM-analisis-mediciones/mediciones/medicion_20230719-015/'

    escalaAceleracion = 9.806/16384
    medicion = Medicion(directory)
    medicion.cambiarEscalaAceleracion(-1,"nodo_94b97eda9150")
    #medicion.cambiarEscalaAceleracion(-1)
    medicion.quitarMediaAceleracion()
    medicion.cambiarEscalaAceleracion(escalaAceleracion)
    
    medicion.correlacionConImpulso(largo, ordenFiltro, wc)

    medicion.graficarCorrelacion()