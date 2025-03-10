from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from model.DAO.add_person_DAO import CitaDAO
from views.doctors_dashboard import Ui_DoctorsDashboard # Asegúrate de importar correctamente tu UI


class MedicoDashboardController(QMainWindow):
    def __init__(self, main_window, usuario_nombre, medico_id):
        super().__init__()
        self.ui = Ui_DoctorsDashboard()
        self.ui.setupUi(main_window)
        self.dao = CitaDAO()
        self.medico_id = medico_id

        self.ui.lb_name_title.setText(usuario_nombre)
        self.ui.lb_id_title.setText(f"ID: {medico_id}")

        # Cargar citas asignadas al médico
        self.load_appointments()

        self.ui.bt_update_appointment.clicked.connect(self.update_appointment_status)
        self.ui.bt_logout.clicked.connect(self.logout)

    def load_appointments(self):
        """Carga las citas del médico en la tabla."""
        try:
            print("Cargando citas del médico...")
            citas = self.dao.obtener_citas_medico(self.medico_id)

            if not citas:
                print("No hay citas registradas para este médico.")

            self.ui.tb_doctor_appointments.setRowCount(0)

            for i, cita in enumerate(citas):
                self.ui.tb_doctor_appointments.insertRow(i)
                self.ui.tb_doctor_appointments.setItem(i, 0, QTableWidgetItem(str(cita.get("nombre_paciente", ""))))
                self.ui.tb_doctor_appointments.setItem(i, 1, QTableWidgetItem(cita.get("fecha", "")))
                self.ui.tb_doctor_appointments.setItem(i, 2, QTableWidgetItem(cita.get("hora", "")))
                self.ui.tb_doctor_appointments.setItem(i, 3, QTableWidgetItem(cita.get("estado", "")))
                self.ui.tb_doctor_appointments.setItem(i, 4, QTableWidgetItem(cita.get("motivo", "")))

        except Exception as e:
            self.show_error(f"Error al cargar citas: {e}")

    def update_appointment_status(self):
        selected_row = self.ui.tb_doctor_appointments.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione una cita para actualizar su estado")
            return

        cita_id = self.ui.tb_doctor_appointments.item(selected_row, 0).text()
        nuevo_estado = self.ui.cb_status_selection.currentText()

        success = self.dao.actualizar_estado_cita(cita_id, nuevo_estado)

        if success:
            QMessageBox.information(self, "Éxito", "Estado de la cita actualizado correctamente")
            self.load_appointments()  # Recargar la tabla
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el estado de la cita")

    def logout(self):
        self.close()  # Aquí puedes redirigir a la pantalla de login

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
