import os, math
import struct


class Nodo:
    def __init__(self, dirName) -> None:
        #si no existe el directori, sale
        if not os.path.exists(dirName):
            print("ERROR: No existe el directorio")
            exit()
        
        #define los atributos basicos de la Medicion
        self.separator='/'#'\\'
        self.dirName = dirName
        dirObjects = dirName.split(self.separator)

        self.nodo = dirObjects.pop(-1)
        self.medicion = dirObjects.pop(-2)

        self.accelerationX_index = 0
        self.accelerationY_index = 1
        self.accelerationZ_index = 2

        self.temp_index = 3

        self.gyroscopeX_index = 4
        self.gyroscopeY_index = 5
        self.gyroscopeZ_index = 5

        self.accelerationX = []
        self.accelerationY = []
        self.accelerationZ = []

        self.temp = []

        self.gyroscopeX = []
        self.gyroscopeY = []
        self.gyroscopeZ = []

        #Las muestras se guardan de a 14 bytes
        self.BYTES_MUESTRA = 14
        #Los primeros 23 bytes corresponden al encabezado y se tiran
        self.BYTES_ENCABEZADO = 23
        
        self.cantArchivos = self.cantidadArchivos()

        self.leerMediciones()

        #self.cantMuestras = self.cantidadMuestras()
    
    def __str__(self) -> str:
        return self.nodo

    def leerMediciones(self) -> None:
        #Busca todos los archivos dentro del directorio para apendearlos a la medicion
        #El ESP genera archivos de a 3000 mediciones (1min de grabacion)
        dirList = os.listdir(self.dirName)
        for archivo in dirList:
            if archivo.split('.')[-1] == "dat":
                self.leerArchivoMediciones(os.path.join(self.dirName, archivo))
    
    def leerArchivoMediciones(self, fileName) -> None:
        file = open(fileName,"rb")
        file.read(self.BYTES_ENCABEZADO) #tira los datos del encabezado


        muestra = file.read(self.BYTES_MUESTRA)
        while muestra:
            #por cada byte que lee lo apendea
            self.leerMuestra(muestra)
            muestra = file.read(self.BYTES_MUESTRA)
        
        file.close()

    def leerMuestra(self, muestra) -> None:
        if len(muestra) != self.BYTES_MUESTRA :
            return
            
        # toma bytes de a dos valores uint8 + uint8 -> int16
        listaMuestras = struct.unpack('7h', muestra)

        # cada linea leida tiene las muestras accelerationX accelerationY accelerationZ temp gyroscopeX gyroscopeY gyroscopeZ
        
        self.accelerationX.append(listaMuestras[self.accelerationX_index])
        self.accelerationY.append(listaMuestras[self.accelerationY_index])
        self.accelerationZ.append(listaMuestras[self.accelerationZ_index])

        self.temp.append(listaMuestras[self.temp_index]/340 + 36.53)

        self.gyroscopeX.append(listaMuestras[self.gyroscopeX_index])
        self.gyroscopeY.append(listaMuestras[self.gyroscopeY_index])
        self.gyroscopeZ.append(listaMuestras[self.gyroscopeZ_index])

    def cambiarEscalaGyroscopo(self, escala) -> None:
        self.gyroscopeX = [ x/escala for x in self.gyroscopeX]
        self.gyroscopeY = [ x/escala for x in self.gyroscopeY]
        self.gyroscopeZ = [ x/escala for x in self.gyroscopeZ]

    def cambiarEscalaAcelerometro(self, escala) -> None:
        self.accelerationX = [ x/escala for x in self.accelerationX]
        self.accelerationY = [ x/escala for x in self.accelerationY]
        self.accelerationZ = [ x/escala for x in self.accelerationZ]
    
    def cantidadMuestras(self,fileName) -> int:
        # numero de muestras tomadas
        cantMuestras = math.ceil(os.fstat(fileName.fileno()).st_size / self.BYTES_MUESTRA)
        cantMuestras -=2
        return cantMuestras
    
    def cantidadArchivos(self) -> int:
        cantidad = 0
        # Iterate directory
        for archivo in self.dirName:
            # check if current path is a file
            if os.path.isfile(os.path.join(self.dirName, archivo)):
                cantidad += 1
        return cantidad
    