from Nodo import Nodo
import os

class Medicion:
    def __init__(self, dirName) -> None:
        #si no existe el directorio, sale
        if not os.path.exists(dirName):
            print("ERROR: No existe el directorio")
            exit()

        #define los atributos basicos de la Medicion
        self.separator='/'#'\\'
        self.carpetaMedicion = dirName
        if self.carpetaMedicion[-1] == self.separator:
            self.carpetaMedicion = self.carpetaMedicion[:-1] #remove trailing slash

        dirObjects = dirName.split(self.separator)

        self.nombreMedicion = dirObjects[-1]


        self.listaNodos = []

        self.agregarNodos()

        print(self.listaNodos)
        
    def agregarNodos(self) -> None:
        listaCarpetaNodos = next(os.walk(self.carpetaMedicion))[1]

        for carpetaNodo in listaCarpetaNodos:
            direccionNodo = os.path.join(self.carpetaMedicion, carpetaNodo)
            self.listaNodos.append(Nodo(direccionNodo))

        

    def cantidadArchivos(self) -> int:
        
        cantidad = 0
        # Iterate directory
        for archivo in self.dirName:
            # check if current path is a file
            if os.path.isfile(os.path.join(self.dirName, archivo)):
                cantidad += 1
        return cantidad
