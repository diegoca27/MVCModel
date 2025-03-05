class Cita:
    def __init__(self, id_cita, paciente, medico, fecha, hora, motivo, estado="pendiente"):
        self.id_cita = id_cita
        self.paciente = paciente
        self.medico = medico
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.estado = estado
        self.signos_vitales = None  # Se actualizará cuando la enfermera registre los signos vitales

    def actualizar_estado(self, nuevo_estado):
        if nuevo_estado in ["confirmada", "pendiente", "cancelada"]:
            self.estado = nuevo_estado
        else:
            print("Estado no válido.")

    def registrar_signos_vitales(self, signos):
        self.signos_vitales = signos

    def __str__(self):
        return f"Cita {self.id_cita}: {self.paciente.nombre} con {self.medico.nombre} el {self.fecha} a las {self.hora} - Estado: {self.estado}"

