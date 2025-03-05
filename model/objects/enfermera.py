from usuario import Usuario

class Enfermera(Usuario):
    def __init__(self, id, nombre, edad, area):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.area = area
        
        super().__init__(id, nombre)

    def actualizarEstadoCita(self, cita, nuevo_estado):
        cita.estado = nuevo_estado

    def registrarSignosVitales(self, cita, signos):
        cita.signos_vitales = signos

    def asistirMedico(self):
        return "Asistiendo al médico"
    
    def registrar_signos(self, cita, signos):
        cita.registrar_signos_vitales(signos)
