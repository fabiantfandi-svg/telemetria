from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
# Importamos la función de inicialización
from telemetria.firebase_config import initialize_firebase

class FirebaseUser:
    def __init__(self, uid, email, rol):
        self.uid = uid
        self.email = email
        self.rol = rol
        self.is_authenticated = True

    def __str__(self):
        return f"{self.email} ({self.rol})"

class FirebaseAuthentication(BaseAuthentication):
    """
    Valida el Token de Firebase y extrae el rol desde la colección 'perfiles' de Firestore.
    """
    def authenticate(self, request):
        # 1. Obtener el header
        auth_header = request.META.get('HTTP_AUTHORIZATION') or request.headers.get('Authorization')
        
        if not auth_header:
            return None 

        partes = auth_header.split()
        if len(partes) != 2 or partes[0].lower() != 'bearer':
            raise AuthenticationFailed("Formato de token inválido")
        
        token = partes[1]

        try:
            # 2. Inicializar DB dentro del try para asegurar disponibilidad
            db = initialize_firebase()

            # 3. Verificar el token con Google
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')

            # 4. Buscar el rol en Firestore (Colección 'perfiles')
            # IMPORTANTE: Asegúrate de que el UID coincida con el nombre del documento en Firebase
            user_profile = db.collection('usuarios').document(uid).get()
            
            if user_profile.exists:
                data = user_profile.to_dict()
                # Extraemos el rol, limpiamos espacios y convertimos a minúsculas
                # Usamos .get('rol') porque es lo que definiste en la base de datos
                rol_db = data.get('rol') or data.get('role') or 'usuario_base'
                rol = str(rol_db).strip().lower()
            else:
                # Si no existe el perfil, podrías imprimir un log para debug
                print(f"DEBUG: No se encontró perfil para UID: {uid}")
                rol = 'usuario_base'

            # 5. Retornar el usuario y el token validado
            return (FirebaseUser(uid, email, rol), decoded_token)
        
        except Exception as e:
            # Imprime el error real en la terminal para que sepas si es Firestore o el Token
            print(f"Error de Autenticación: {str(e)}")
            raise AuthenticationFailed(f"Token inválido o error de servidor: {str(e)}")