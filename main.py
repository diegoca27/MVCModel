# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from views.login_hospital import UI_LoginWindow
from views.patients_dashboard import UI_PatientsDashboard
from views.doctors_dashboard import Ui_DoctorsDashboard
from views.nurse_dashboard import UI_NurseDashboard
from views.administrator_dashboard import UI_AdminDashboard
from model.DAO.add_person_DAO import CitaDAO
from controllers.citaController import CitaController
from controllers.nurseController import NurseDashboardController
from controllers.medicController import MedicoDashboardController


class HospitalApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        
        # Inicialmente cargar la vista de login
        self.iniciar_login()
        
        self.main_window.show()
        sys.exit(self.app.exec_())
    
    def iniciar_login(self):
        # Configurar la UI de login
        self.current_ui = UI_LoginWindow()
        self.current_ui.setupUi(self.main_window)
        
        # Iniciar el controlador de login y conectar señales
        self.login_controller = CitaDAO()
        
        # Conectar la función de login exitoso con la de redirección
        # Ejemplo usando botón de login
        self.current_ui.btn_login.clicked.connect(self.verificar_login)
    
    def verificar_login(self):
        # Obtener datos de los campos de login
        nombre = self.current_ui.txt_name.toPlainText().strip()
        usuario_id = self.current_ui.txt_id.toPlainText().strip()
        rol = self.current_ui.cmb_role.currentText()
        
        dao = CitaDAO()
        usuario_valido = dao.verificar_credenciales(nombre, usuario_id, rol)
        
        if usuario_valido:
            # Redirigir según el rol
            self.redirigir_por_rol(rol, usuario_id, nombre)
        else:
            # Mostrar mensaje de error
            QMessageBox.critical(self.main_window, "Error", "Credenciales incorrectas")
    
    def redirigir_por_rol(self, rol, usuario_id, nombre):
        """
        Redirige a la vista correspondiente según el rol del usuario.
        """
        self.limpiar_ui()

        try:
            # Seleccionar la vista según el rol
            if rol == "Paciente":
                self.current_ui = UI_PatientsDashboard()
                self.current_ui.setupUi(self.main_window)

                # Establecer la información del usuario
                self.current_ui.lb_name_title.setText(nombre)
                self.current_ui.lb_id_title.setText(f"ID: {usuario_id}")

                # ✅ Pasar el dashboard correcto al controlador
                self.cita_controller = CitaController(self.current_ui, usuario_id)

                # Cargar citas del paciente
                citas = self.cita_controller.cargar_citas()
                if citas:
                    for cita in citas:
                        print("📅 Cita encontrada:", cita)
                else:
                    print("❌ No se encontraron citas para el paciente.")

            elif rol == "Médico":
                self.current_ui = Ui_DoctorsDashboard()
                self.current_ui.setupUi(self.main_window)
                self.medic_controller = MedicoDashboardController(self.main_window, nombre, usuario_id)


            elif rol == "Enfermera":
                self.current_ui = UI_NurseDashboard()
                self.current_ui.setupUi(self.main_window)
                self.nurse_controller = NurseDashboardController(self.main_window, nombre, usuario_id)
                self.current_ui.lb_name_title.setText(nombre)
                self.current_ui.lb_id_title.setText(f"ID: {usuario_id}")

            elif rol == "Administrador":
                self.current_ui = UI_AdminDashboard()
                self.current_ui.setupUi(self.main_window)

            else:
                QMessageBox.warning(self.main_window, "Error", "Rol no reconocido.")
                return

            # Conectar el botón de cerrar sesión
            if hasattr(self.current_ui, 'bt_logout'):
                self.current_ui.bt_logout.clicked.connect(self.iniciar_login)

        except Exception as e:
            print(f"❌ Error al redirigir por rol: {e}")
            QMessageBox.critical(self.main_window, "Error", f"Error al cargar la interfaz: {e}")
    
    def limpiar_ui(self):
        # Eliminar todos los widgets del layout central
        if self.main_window.centralWidget() is not None:
            old_widget = self.main_window.centralWidget()
            old_widget.setParent(None)

if __name__ == "__main__":
    app = HospitalApp()