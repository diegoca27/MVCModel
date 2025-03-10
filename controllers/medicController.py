from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from model.DAO.add_person_DAO import CitaDAO
from views.doctors_dashboard import Ui_DoctorsDashboard


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

        self.ui.bt_update_appointment.clicked.connect(self.update_appointment)
        self.ui.bt_confirm_appointment.clicked.connect(self.confirm_appointment)

        # self.ui.bt_logout.clicked.connect(self.logout)

    def load_appointments(self):
        """Carga las citas del médico en la tabla."""
        try:
            print("Cargando citas del médico...")
            citas = self.dao.get_medic_appointments(self.medico_id)

            if not citas:
                print("No hay citas registradas para este médico.")

            self.ui.tb_doctor_appointments.setRowCount(0)

            for i, cita in enumerate(citas):
                cita_id = cita["id"]
                self.ui.tb_doctor_appointments.insertRow(i)
                self.ui.tb_doctor_appointments.setItem(i, 0, QTableWidgetItem(str(cita.get("nombre_paciente", ""))))
                self.ui.tb_doctor_appointments.setItem(i, 1, QTableWidgetItem(cita.get("fecha", "")))
                self.ui.tb_doctor_appointments.setItem(i, 2, QTableWidgetItem(cita.get("hora", "")))
                self.ui.tb_doctor_appointments.setItem(i, 3, QTableWidgetItem(cita.get("estado", "")))
                self.ui.tb_doctor_appointments.setItem(i, 4, QTableWidgetItem(cita.get("motivo", "")))

                item_paciente = self.ui.tb_doctor_appointments.item(i, 0)
                item_paciente.setData(Qt.UserRole, cita_id)

        except Exception as e:
            print(e)
            self.show_error(f"Error al cargar citas: {e}")

    def update_appointment(self):
        selected_row = self.ui.tb_doctor_appointments.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione una cita para actualizar su estado")
            return

        item_paciente = self.ui.tb_doctor_appointments.item(selected_row, 0)
        cita_id = item_paciente.data(Qt.UserRole)
        success = self.dao.confirm_appointment(cita_id)

        # TODO: Add update appointment logic
        # ...

        if success:
            QMessageBox.information(self, "Éxito", "Cita actualizada correctamente")
            self.load_appointments()
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar la cita")

    def confirm_appointment(self):
        selected_row = self.ui.tb_doctor_appointments.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione una cita para actualizar su estado")
            return
        
        item_paciente = self.ui.tb_doctor_appointments.item(selected_row, 0)
        cita_id = item_paciente.data(Qt.UserRole)
        success = self.dao.confirm_appointment(cita_id)

        if success:
            QMessageBox.information(self, "Éxito", "Estado de la cita actualizado correctamente")
            self.load_appointments()
        else:
            QMessageBox.warning(self, "Error", "No se pudo actualizar el estado de la cita")

    def logout(self):
        self.close()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
