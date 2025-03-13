from PyQt5.QtWidgets import QMessageBox
from dbConnection.firebase_config import db
from google.cloud.firestore import Query

class CitaDAO:
    def __init__(self):
        self.citas_ref =  db.collection("citas")
        self.usuarios_ref = db.collection("usuarios")

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

    def verificar_credenciales(self, nombre, usuario_id, rol):
        try:
            # Intentamos convertir a entero si está almacenado como número
            try:
                usuario_id_num = int(usuario_id)
            except ValueError:
                usuario_id_num = usuario_id
            
            # Consultar documentos de usuarios
            documentos = self.usuarios_ref.stream()
            
            # Buscar coincidencia
            for doc in documentos:
                datos = doc.to_dict()
                if ((datos.get("id") == usuario_id or datos.get("id") == usuario_id_num) and
                    datos.get("nombre") == nombre and
                    datos.get("rol") == rol):
                    return True
            
            # Si no se encontró coincidencia
            return False
            
        except Exception as e:
            print(f"Error al verificar credenciales: {e}")
            return False

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

    def crear_cita(self, cita):
        try:
            nueva_cita = self.citas_ref.add(cita)
            print("Cita creada:", nueva_cita[1])
            return nueva_cita
        except Exception as e:
            print(f"Error al crear la cita: {e}")
            return None

    def obtener_cita(self, usuario_id):
        try:
            # Asegurar que usuario_id sea un entero para la consulta
            if isinstance(usuario_id, str):
                usuario_id = int(usuario_id)

            citas = self.citas_ref.where("usuario_id", "==", usuario_id).stream()
            lista_citas = []

            for cita in citas:
                datos = cita.to_dict()
                lista_citas.append(datos)

            return lista_citas

        except Exception as e:
            print(f"Error al obtener las citas: {e}")
            return []

    def obtener_todas_las_citas(self):
        try:
            # Obtener todos los usuarios en un diccionario {id: nombre}
            usuarios = {}
            for doc in self.usuarios_ref.stream():
                usuario_data = doc.to_dict()
                usuario_id = usuario_data.get("id")
                if usuario_id is not None:  # Verificar que el ID no sea None
                    usuarios[usuario_id] = usuario_data.get("nombre", "Desconocido")

            # Obtener todas las citas
            citas = self.citas_ref.stream()
            lista_citas = []

            for cita in citas:
                cita_data = cita.to_dict()
                usuario_id = cita_data.get("usuario_id")

                # Obtener el nombre del usuario desde el diccionario en memoria
                nombre_usuario = usuarios.get(usuario_id, "Desconocido")

                # Agregar el nombre a la cita
                cita_data["nombre_paciente"] = nombre_usuario
                lista_citas.append(cita_data)

            print(f"Total de citas encontradas: {len(lista_citas)}")
            return lista_citas

        except Exception as e:
            print(f"Error al obtener las citas: {e}")
            return []
    
    def get_medic_appointments(self, medico_id):
        """Obtiene todas las citas asignadas a un médico específico."""
        try:
            citas = self.citas_ref.where("medico_id", "==", medico_id).stream()
            lista_citas = []

            for cita in citas:
                cita_data = cita.to_dict()
                paciente_id = cita_data.get("usuario_id")

                # Obtener el nombre del paciente
                usuario_doc = self.usuarios_ref.document(str(paciente_id)).get()
                nombre_paciente = usuario_doc.to_dict().get("nombre", "Desconocido") if usuario_doc.exists else "Desconocido"

                # Agregar el nombre del paciente a la cita
                cita_data["nombre_paciente"] = nombre_paciente
                cita_data["id"] = cita.id
                lista_citas.append(cita_data)

            print(f"Total de citas encontradas para el médico {medico_id}: {len(lista_citas)}")
            print(lista_citas)
            return lista_citas

        except Exception as e:
            print(f"Error al obtener citas del médico {medico_id}: {e}")
            return []
        

    def actualizar_signos_vitales(self, usuario_id, signos_vitales):
        try:
            # Primero intentamos convertir el usuario_id a entero si está almacenado como número
            try:
                usuario_id_num = int(usuario_id)
            except ValueError:
                usuario_id_num = usuario_id
                
            # Buscar el usuario por su ID (probando ambos tipos: string y numérico)
            usuarios = self.usuarios_ref.stream()
            
            usuario_encontrado = False
            for usuario in usuarios:
                datos = usuario.to_dict()
                # Verificamos con ambos tipos (string y número)
                if datos.get("id") == usuario_id or datos.get("id") == usuario_id_num:
                    usuario_ref = self.usuarios_ref.document(usuario.id)
                    
                    # Actualizar los signos vitales en el perfil del usuario
                    usuario_ref.update({
                        "pulsaciones": signos_vitales.get("pulsaciones", 0),
                        "presion": signos_vitales.get("presion", "120/80"),
                        "temperatura": signos_vitales.get("temperatura", 36.5)
                    })
                    
                    print(f"Signos vitales actualizados correctamente para el usuario {usuario_id}.")
                    usuario_encontrado = True
                    
                    # También actualizar la cita si existe (para mantener registro histórico)
                    citas = self.citas_ref.where("usuario_id", "==", datos.get("id")).stream()
                    for cita in citas:
                        cita_ref = self.citas_ref.document(cita.id)
                        cita_ref.update({"signos_vitales": signos_vitales})
                        print("Signos vitales también actualizados en la cita.")
                    break
            
            if not usuario_encontrado:
                print(f"No se encontró un usuario con ID {usuario_id}.")
                return False
                
            return usuario_encontrado

        except Exception as e:
            print(f"Error al actualizar los signos vitales: {e}")
            return False
        
    def obtener_todos_los_pacientes(self):
        """Devuelve una lista de todos los pacientes en Firestore."""
        try:
            pacientes = []
            usuarios = self.usuarios_ref.stream()

            for usuario in usuarios:
                usuario_data = usuario.to_dict()
                if usuario_data.get("rol") == "Paciente":  # ✅ Solo pacientes
                    pacientes.append({
                        "id": usuario_data.get("id"),
                        "nombre": usuario_data.get("nombre")
                    })

            return pacientes

        except Exception as e:
            print(f"❌ Error al obtener los pacientes: {e}")
            return []
        
    def confirm_appointment(self, cita_id):
        """Cambia el estado de una cita a 'Confirmada' en Firestore."""
        try:
            cita_ref = self.citas_ref.document(cita_id)
            cita_ref.update({"estado": "Confirmada"})

            print(f"✅ Cita {cita_id} confirmada exitosamente.")
            return True

        except Exception as e:
            print(f"❌ Error al confirmar la cita {cita_id}: {e}")
            return False
        
    def update_appointment(self, cita_id, updated_cita):
        try:
            # Get the document reference for the specific appointment
            cita_ref = self.citas_ref.document(cita_id)

            # Update the appointment with the new data
            cita_ref.update(updated_cita)

            print(f"✅ Cita {cita_id} actualizada exitosamente.")
            return True
        
        except Exception as e:
            print(f"❌ Error al actualizar la cita {cita_id}: {e}")
            return False

        

    def get_patient(self, patient_id):
            """Obtiene el nombre del paciente usando su 'id' en el campo 'id'."""
            try:
                # Query the 'patients' collection to find a document where the field 'id' matches patient_id
                patient_ref = self.usuarios_ref.where("id", "==", int(patient_id)).limit(1)
                patient_docs = patient_ref.stream()

                # Get the first matching document (if any)
                for patient_doc in patient_docs:
                    print("Patient found: ", patient_doc.to_dict())  # You can print the entire document
                    return patient_doc.to_dict()

                # If no document found, handle it accordingly
                print(f"No patient found with id: {patient_id}")
                return None
            except Exception as e:
                print(f"Error while fetching patient: {e}")
                return None
