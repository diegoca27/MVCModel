from PyQt5.QtWidgets import QMessageBox
from dbConnection.firebase_config import db
from google.cloud.firestore import Query

class LoginController:
    def __init__(self, ui):
        self.ui = ui
        self.ui.btn_login.clicked.connect(self.login)

    def login(self):
        nombre = self.ui.txt_name.toPlainText().strip()
        usuario_id = self.ui.txt_id.toPlainText().strip()
        rol = self.ui.cmb_role.currentText()

        print("Nombre recibido:", nombre)
        print("ID recibido:", usuario_id)
        print("Rol:", rol)
        
        if not nombre or not usuario_id:
            self.mostrar_error("Debe completar todos los campos.")
            return
        
        try:
            # Convertimos usuario_id a entero si está almacenado como número en la BD
            try:
                usuario_id_num = int(usuario_id)
            except ValueError:
                # Si no se puede convertir, mantenemos el valor original
                usuario_id_num = usuario_id
            
            usuarios_ref = db.collection("usuarios")
            documentos = usuarios_ref.stream()
            
            usuario_encontrado = None
            for doc in documentos:
                datos = doc.to_dict()
                # Verificamos con ambos tipos (string y número)
                if ((datos.get("id") == usuario_id or datos.get("id") == usuario_id_num) and 
                    datos.get("nombre") == nombre and 
                    datos.get("rol") == rol):
                    usuario_encontrado = datos
                    break
            
            if usuario_encontrado:
                self.mostrar_mensaje(f"Bienvenido {nombre} ({rol})")
                self.redirigir_por_rol(rol, usuario_id, nombre)
            else:
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
