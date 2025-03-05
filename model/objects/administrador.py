from usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id, nombre):
        super().__init__(id, nombre, "Administrador")

    def visualizarCitas(self, citas):
        return citas
    
    def gestionarHorarios(self):
        return "Gestionando usuarios"