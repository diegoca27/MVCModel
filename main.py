import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from views.login_hospital import Ui_MainWindow   # Importa la clase generada

class Controlador(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear una instancia de la UI
        self.ui = Ui_MainWindow()

        # Configurar la UI en esta ventana
        self.ui.setupUi(self)

        # Conectar el botón a una función
        self.ui.btn_login.clicked.connect(self.iniciar_sesion)

    def iniciar_sesion(self):
        nombre = self.ui.txt_name.toPlainText()
        id_usuario = self.ui.txt_id.toPlainText()
        rol = self.ui.cmb_role.currentText()

        print(f"Nombre: {nombre}")
        print(f"ID: {id_usuario}")
        print(f"Rol: {rol}")

        if nombre and id_usuario:
            print("✅ Inicio de sesión exitoso")
        else:
            print("❌ Por favor, complete todos los campos.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear una instancia del controlador
    ventana = Controlador()
    ventana.show()

    sys.exit(app.exec_())