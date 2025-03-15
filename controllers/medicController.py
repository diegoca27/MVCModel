from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QDate, QTime
from model.DAO.add_person_DAO import CitaDAO
from views.doctors_dashboard import Ui_DoctorsDashboard
from views.appointment_update import Ui_UpdateAppointmentWindow


class MedicoDashboardController(QMainWindow):
    def __init__(self, main_window, usuario_nombre, medico_id, main_app):
        super().__init__()
        self.ui = Ui_DoctorsDashboard()
        self.ui.setupUi(main_window)
        self.dao = CitaDAO()
        self.medico_id = medico_id
        self.main_app = main_app

        self.ui.lb_name_title.setText(usuario_nombre)
        self.ui.lb_id_title.setText(f"ID: {medico_id}")

        # Cargar citas asignadas al médico
        self.load_appointments()

        self.ui.cb_status_filter.currentIndexChanged.connect(self.filter_appointments)

        self.ui.bt_update_appointment.clicked.connect(self.update_appointment)
        self.ui.bt_confirm_appointment.clicked.connect(self.confirm_appointment)

        self.ui.bt_logout.clicked.connect(self.logout)

    
    def load_appointments(self, status_filter=None):
        """Loads the appointments into the table, optionally filtering by status."""
        try:
            print("Cargando citas del médico...")
            citas = self.dao.get_medic_appointments(self.medico_id)

            if not citas:
                print("No hay citas registradas para este médico.")

            self.ui.tb_doctor_appointments.setRowCount(0)  # Clear table before loading new data
            
            row_index = 0  # Use a separate counter for table rows
            
            for cita in citas:
                if status_filter and cita.get("estado") != status_filter:
                    continue  # Skip if status doesn't match filter
                    
                cita_id = cita["id"]
                patient = self.dao.get_patient(cita.get("usuario_id"))
                
                self.ui.tb_doctor_appointments.insertRow(row_index)
                self.ui.tb_doctor_appointments.setItem(row_index, 0, QTableWidgetItem(patient["nombre"]))
                self.ui.tb_doctor_appointments.setItem(row_index, 1, QTableWidgetItem(cita.get("fecha", "")))
                self.ui.tb_doctor_appointments.setItem(row_index, 2, QTableWidgetItem(cita.get("hora", "")))
                self.ui.tb_doctor_appointments.setItem(row_index, 3, QTableWidgetItem(cita.get("estado", "")))
                self.ui.tb_doctor_appointments.setItem(row_index, 4, QTableWidgetItem(cita.get("motivo", "")))

                item_paciente = self.ui.tb_doctor_appointments.item(row_index, 0)
                item_paciente.setData(Qt.UserRole, cita_id)
                
                row_index += 1  # Increment only when a row is actually added

        except Exception as e:
            print(e)
            self.show_error(f"Error al cargar citas: {e}")

    def filter_appointments(self):
        """Applies the selected status filter to the appointments table."""
        selected_status = self.ui.cb_status_filter.currentText()
        
        if selected_status == "Todos":
            selected_status = None  # Load all appointments
        
        self.load_appointments(status_filter=selected_status)

    def update_appointment(self):
        selected_row = self.ui.tb_doctor_appointments.currentRow()

        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione una cita para actualizar su estado")
            return

        #Get the selected row's appointment ID
        item_paciente = self.ui.tb_doctor_appointments.item(selected_row, 0)
        appointment_id = item_paciente.data(Qt.UserRole)

        #Get the appointment data from the table directly (no need to query again)
        paciente_nombre = self.ui.tb_doctor_appointments.item(selected_row, 0).text()
        cita_fecha = self.ui.tb_doctor_appointments.item(selected_row, 1).text()
        cita_hora = self.ui.tb_doctor_appointments.item(selected_row, 2).text()
        cita_estado = self.ui.tb_doctor_appointments.item(selected_row, 3).text()
        cita_motivo = self.ui.tb_doctor_appointments.item(selected_row, 4).text()

        #Open the update appointment window and populate it with the extracted data
        self.update_window = QMainWindow()
        self.current_ui = Ui_UpdateAppointmentWindow()
        self.current_ui.setupUi(self.update_window)

        self.current_ui.lb_patient_name.setText(paciente_nombre)
        print("fecha de cita: ", cita_fecha)
        self.current_ui.date_appointment.setDate(QDate.fromString(cita_fecha, "yyyy/MM/dd"))
        self.current_ui.time_appointment.setTime(QTime.fromString(cita_hora, "HH:mm"))
        self.current_ui.cb_status.setCurrentText(cita_estado) 
        self.current_ui.txt_reason.setText(cita_motivo)

        # Connect the save button to the save_updated_appointment method
        self.current_ui.bt_save.clicked.connect(lambda: self.save_updated_appointment(appointment_id))
        self.update_window.show()

    def save_updated_appointment(self, appointment_id):
        # Get the updated values from the UI
        updated_fecha = self.current_ui.date_appointment.date().toString("yyyy/MM/dd")
        updated_hora = self.current_ui.time_appointment.time().toString("HH:mm")
        updated_estado = self.current_ui.cb_status.currentText()
        updated_motivo = self.current_ui.txt_reason.toPlainText()

        if not updated_fecha or not updated_hora or not updated_estado or not updated_motivo:
            QMessageBox.warning(self, "Error", "Debe completar todos los campos.")
            return

        #dictionary with the updated data
        updated_appointment = {
            "fecha": updated_fecha,
            "hora": updated_hora,
            "estado": updated_estado,
            "motivo": updated_motivo
        }

        # Call the DAO function to update the appointment
        resultado = self.dao.update_appointment(appointment_id, updated_appointment)

        if resultado:
            QMessageBox.information(self, "Éxito", "Cita actualizado correctamente")
            self.update_window.close()
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
        self.main_app.iniciar_login()

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
