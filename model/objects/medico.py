from usuario import Usuario

class Medico(Usuario):
    def __init__(self, id, nombre, especialidad):
        super().__init__(id, nombre, "Medico")
        self.especialidad = especialidad
        self.citas = []
        self.horario_disponible = []

    def revisar_citas(self):
        return self.citas
    
    def actualizar_cita(self, cita, nueva_fecha, nueva_hora, nuevo_motivo):
        if cita in self.citas:
            cita.actualizar_cita(nueva_fecha, nueva_hora, nuevo_motivo)
        else:
            print("No pudimos encontrar la cita.")

    def aceptar_cita(self, cita):
        cita.actualizar_estado("confirmada")

    def agregar_disponibilidad(self, fecha, hora):
        self.horario_disponible.append((fecha, hora))