from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from views.nurse_dashboard import UI_NurseDashboard  # Asegúrate de importar correctamente tu UI
from model.DAO.add_person_DAO import CitaDAO  # Tu DAO para Firestore

class NurseDashboardController(QMainWindow):
    def __init__(self, main_window, usuario_nombre, usuario_id, main_app):
        super().__init__()
        self.ui = UI_NurseDashboard()
        self.ui.setupUi(main_window)
        self.dao = CitaDAO() 
        self.main_app = main_app

        self.ui.lb_name_title.setText(usuario_nombre)
        self.ui.lb_id_title.setText(f"ID: {usuario_id}")

        # Cargar citas en la tabla
        self.load_appointments()
        self.load_patient_list()

        # Conectar botones a sus funciones
        self.ui.bt_register.clicked.connect(self.register_vital_signs)
        self.ui.bt_logout.clicked.connect(self.logout)

        self.ui.bt_assist_dr.clicked.connect(self.assist_doctor)

    def assist_doctor(self):
        """Muestra un mensaje indicando que el doctor ha sido asistido."""
        QMessageBox.information(self, "Asistencia", "Doctor asistido")

    def load_appointments(self):
        try:
            print("Cargando citas...")  # Verificar si la función se ejecuta
            citas = self.dao.obtener_todas_las_citas()

            if not citas:
                print("No hay citas registradas.")  # Si la lista está vacía
                return  # Exit the function if there are no appointments

            # Configurar la tabla
            self.ui.tb_nurse_appointments.setRowCount(0)  # Limpiar tabla
            
            for i, cita in enumerate(citas):
                # Get patient info inside the loop for each appointment
                patient = self.dao.get_patient(cita.get("usuario_id"))
                
                self.ui.tb_nurse_appointments.insertRow(i)
                
                # Check if patient data exists
                if patient and "nombre" in patient:
                    self.ui.tb_nurse_appointments.setItem(i, 0, QTableWidgetItem(patient["nombre"]))
                else:
                    # Use nombre_paciente from the appointment if available, or "Desconocido"
                    self.ui.tb_nurse_appointments.setItem(i, 0, QTableWidgetItem(cita.get("nombre_paciente", "Desconocido")))
                    
                self.ui.tb_nurse_appointments.setItem(i, 1, QTableWidgetItem(cita.get("fecha", "")))
                self.ui.tb_nurse_appointments.setItem(i, 2, QTableWidgetItem(cita.get("hora", "")))
                
        except Exception as e:
            print(f"Error detallado: {e}")  # Add detailed error logging
            QMessageBox.warning(self, "Error", f"Error al cargar citas: {str(e)}")

    def register_vital_signs(self):
        """Guarda los signos vitales del paciente seleccionado en Firestore."""
        # Obtener el índice seleccionado y el usuario_id asociado
        index = self.ui.cb_patient_selection.currentIndex()
        usuario_id = self.ui.cb_patient_selection.itemData(index)

        # Obtener los valores de los signos vitales
        pulsaciones = self.ui.txt_vital_signs.toPlainText()
        presion = self.ui.txt_blood_pressure.toPlainText()
        temperatura = self.ui.txt_temperature.toPlainText()

        # Validar que todos los campos estén completos
        if not usuario_id or not pulsaciones or not presion or not temperatura:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        # Preparar los datos a guardar
        data = {
            "pulsaciones": pulsaciones,
            "presion": presion,
            "temperatura": temperatura
        }

        # Guardar los signos vitales en Firestore
        success = self.dao.actualizar_signos_vitales(usuario_id, data)

        # Mostrar mensaje de confirmación o error
        if success:
            QMessageBox.information(self, "Éxito", "Signos vitales guardados correctamente")
        else:
            QMessageBox.warning(self, "Error", "No se pudo guardar la información")

    def load_patient_list(self):
        """Carga los nombres de los pacientes en el dropdown list."""
        try:
            pacientes = self.dao.obtener_todos_los_pacientes()  # Nueva función en DAO
            self.ui.cb_patient_selection.clear()  # Limpiar dropdown

            for paciente in pacientes:
                nombre = paciente["nombre"]
                usuario_id = int(paciente["id"])
                print("Paciente encontrado:", paciente["nombre"])
                self.ui.cb_patient_selection.addItem(nombre, usuario_id)  # ✅ Agrega nombre y usuario_id oculto

        except Exception as e:
            QMessageBox.warning(self, "Error", "Error al cargar la lista de pacientes")

    def logout(self):
        self.main_app.iniciar_login()

