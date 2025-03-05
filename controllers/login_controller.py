# controllers/login_controller.py

from PyQt5.QtWidgets import QMessageBox
from dbConnection.firebase_config import db

class LoginController:
    def __init__(self, ui):
        self.ui = ui
        self.ui.btn_login.clicked.connect(self.login)

    def login(self):
        nombre = self.ui.txt_name.toPlainText().strip()
        usuario_id = self.ui.txt_id.toPlainText().strip()
        rol = self.ui.cmb_role.currentText()

        if not nombre or not usuario_id:
            self.mostrar_error("Debe completar todos los campos.")
            return

        try:
            usuarios = db.child("usuarios").get()

            for usuario in usuarios.each():
                data = usuario.val()
                if data["id"] == usuario_id and data["nombre"] == nombre and data["rol"] == rol:
                    self.mostrar_mensaje(f"Bienvenido {nombre} ({rol})")
                    self.redirigir_por_rol(rol, usuario_id, nombre)
                    return
            
            self.mostrar_error("Credenciales incorrectas o usuario no registrado.")
        except Exception as e:
            self.mostrar_error(f"Error en la autenticación: {e}")

    def redirigir_por_rol(self, rol, usuario_id, nombre):
        if rol == "Paciente":
            print(f"Redirigiendo a vista de Paciente: {nombre}")
        elif rol == "Médico":
            print(f"Redirigiendo a vista de Médico: {nombre}")
        elif rol == "Enfermera":
            print(f"Redirigiendo a vista de Enfermera: {nombre}")
        elif rol == "Administrador":
            print(f"Redirigiendo a vista de Administrador: {nombre}")

    def mostrar_error(self, mensaje):
        QMessageBox.critical(None, "Error", mensaje)

    def mostrar_mensaje(self, mensaje):
        QMessageBox.information(None, "Éxito", mensaje)
