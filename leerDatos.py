#import matplotlib.pyplot as plt
from Medicion import Medicion
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal



'''
def graficarMediciones(medicion):
    fig, ax = plt.subplots(2,1)

    ax[0].set_title("Acelerometro")
    ax[0].plot(medicion.accelerationX, color='b', linewidth=0.1)
    ax[0].plot(medicion.accelerationY, color='r', linewidth=0.1)
    ax[0].plot(medicion.accelerationZ, color='g', linewidth=0.1)
    
    ax[1].set_title("Temperatura")
    ax[1].plot(medicion.temp, color='b', linewidth=0.1)

    plt.show()
'''
def agregarMediciones(dirName) -> list:
    dirList = os.listdir(dirName)
    listMediciones = []

    for carpeta in dirList:
        dirNodo = os.path.join(dirName, carpeta)  # join the path
        listMediciones.append(Medicion(dirNodo))

    return listMediciones 


def configParser(parser):
    parser.add_argument('-c', '--carpeta', type=str, metavar='dir', dest='meassureDir',
                    help='Crea imagenes de las mediciones en la carpeta indicada')
    parser.add_argument('-l', '--list', type=str, metavar='dir', dest='listDir',
                    help='Lista los archivos de la carpeta indicada')
    
def tiempo(listMediciones):
    # Crear un diccionario a partir de la lista de objetos
    dicc = {medicion.nodo: medicion.accelerationY for medicion in listMediciones}
    df = pd.DataFrame(dicc)
    df.plot(kind='line', y=df.columns[1], title='Tiempo')
    df.plot(kind='line', y=df.columns[0], ax=plt.gca())

    plt.show()

def impulso():
    imp = signal.unit_impulse(500)
    b, a = signal.butter(6, 0.038)
    impulseResponse = signal.lfilter(b, a, imp)

def correlacion(listMediciones):
    # Crear un diccionario a partir de la lista de objetos
    dicc = {medicion.nodo: medicion.accelerationY for medicion in listMediciones}
    df = pd.DataFrame(dicc).astype(float)

    cantPuntos = df[listMediciones[0].nodo].size
    nodo1 = df[listMediciones[0].nodo].to_numpy()
    nodo2 = df[listMediciones[1].nodo].to_numpy()

    corr = signal.correlate(nodo1, nodo2, mode='same') / cantPuntos

    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1)
    ax_orig.plot(nodo1)
    ax_orig.set_title('Nodo 1')

    ax_noise.plot(nodo2)
    ax_noise.set_title('Nodo2')

    ax_corr.plot(corr)
    ax_corr.axhline(0.5, ls=':')
    ax_corr.set_title('Cross-correlated with rectangular pulse')
    ax_orig.margins(0, 0.1)
    fig.tight_layout()
    plt.show()



    
def main():
    ESCALA_ACELERACION = 16384
    ESCALA_GIROSCOPO = 131

    parser = argparse.ArgumentParser(prog='leer-mediciones')
    configParser(parser)
    args=vars(parser.parse_args())
    
    if args['meassureDir'] is not None :
        dirName = args['meassureDir']

        listMediciones = agregarMediciones(dirName)
    
        for medicion in listMediciones:
            medicion.leerMediciones()
            medicion.cambiarEscalaGyroscopo(ESCALA_GIROSCOPO)
            medicion.cambiarEscalaAcelerometro(ESCALA_ACELERACION)


    elif args['listDir'] is not None:
        dirName = args['listDir']
        return os.listdir(dirName)

    if not dirName:
        raise SystemExit(f"Ingrese carpeta con mediciones") 
    
    if not os.path.isdir(dirName):
        raise SystemExit(f"No existe la carpeta \"{dirName}\"") 
    
    correlacion(listMediciones)

    

    


if __name__ == '__main__':

    main()