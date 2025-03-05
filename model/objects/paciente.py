from usuario import Usuario
from cita import Cita

class Paciente(Usuario):
    def __init__(self, id, nombre):
        super().__init__(id, nombre, "Paciente")
        self.citas = []

    def agendar_cita(self, medico, fecha, hora, motivo):
        if (fecha, hora) in medico.horario_disponible:
            cita = Cita(len(self.citas) + 1, self, medico, fecha, hora, motivo)
            self.citas.append(cita)
            medico.citas.append(cita)
            medico.horario_disponible.remove((fecha, hora))  # Bloquear el horario
            return cita
        else:
            print("El médico no está disponible en ese horario.")
            return None

    def ver_citas(self):
        return [str(cita) for cita in self.citas]
