from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from model.DAO.add_person_DAO import CitaDAO

class CitaController:
    def __init__(self, ui, usuario_id):
        self.ui = ui
        self.ui.bt_appointment.clicked.connect(self.agendar_cita)
        self.dao = CitaDAO()
        self.usuario_id = usuario_id

    def agendar_cita(self):
        fecha = self.ui.txt_date.toPlainText().strip()
        hora = self.ui.txt_hour.toPlainText().strip()
        estado = self.ui.txt_status.toPlainText().strip()
        motivo = self.ui.txt_reason.toPlainText().strip()
        print("Agendando cita...")

        if not fecha or not hora or not estado or not motivo:
            self.mostrar_error("Debe completar todos los campos.")
            return

        cita = {
            "usuario_id":self.usuario_id,
            "fecha": fecha,
            "hora": hora,
            "estado": estado,
            "motivo": motivo
        }

        resultado = self.dao.crear_cita(cita)
        if resultado:
            self.mostrar_mensaje("Cita creada con éxito.")
        else:
            self.mostrar_error("Error al crear la cita.")

    def cargar_citas(self):
        citas = self.dao.obtener_cita(self.usuario_id)
        self.ui.tb_patient_appointments.setRowCount(len(citas))  # Ajustar tamaño de la tabla

        for row, cita in enumerate(citas):
            self.ui.tb_patient_appointments.setItem(row, 0, QTableWidgetItem(cita["fecha"]))
            self.ui.tb_patient_appointments.setItem(row, 1, QTableWidgetItem(cita["hora"]))
            self.ui.tb_patient_appointments.setItem(row, 2, QTableWidgetItem(cita["estado"]))
            self.ui.tb_patient_appointments.setItem(row, 3, QTableWidgetItem(cita["motivo"]))

    def mostrar_error(self, mensaje):
        QMessageBox.critical(None, "Error", mensaje)

    def mostrar_mensaje(self, mensaje):
        QMessageBox.information(None, "Éxito", mensaje)