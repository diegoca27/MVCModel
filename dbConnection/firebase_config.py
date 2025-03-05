import os
import firebase_admin
from firebase_admin import credentials, firestore

class FirebaseConnection:
    def __init__(self):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(base_dir, "mvc-model-firebase-adminsdk-fbsvc-8794cd2a17.json")

            if not os.path.exists(json_path):
                print(f"❌ Credential file not found in {json_path}")
                raise FileNotFoundError(f"Credential file not found in {json_path}")

            if not firebase_admin._apps:
                cred = credentials.Certificate(json_path)
                firebase_admin.initialize_app(cred)
                print("✅ Conexión a Firebase exitosa.")

            # Conectar con Firestore
            self.db = firestore.client()

        except Exception as e:
            print(f"❌ Error al conectar con Firebase: {e}")
            self.db = None

# Instancia de conexión
firebase_connection = FirebaseConnection()
db = firebase_connection.db