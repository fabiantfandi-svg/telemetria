import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, firestore
from telemetria.firebase_config import initialize_firebase

db = initialize_firebase()



class RegistroAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('rol')  # viene como "rol" del frontend
 
        if not email or not password or not role:
            return Response(
                {"error": "Faltan datos (email, password, rol)"},
                status=status.HTTP_400_BAD_REQUEST
            )
 
        role = str(role).strip().lower()

        # 🔥 ROLES CORRECTOS PARA TU PROYECTO
        if role not in ['sensor', 'admin']:
            return Response(
                {"error": "Rol inválido. Usa 'sensor' o 'admin'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 🔥 Crear usuario en Firebase Auth
            user = auth.create_user(
                email=email,
                password=password
            )

            # 🔥 Guardar perfil en Firestore
            db.collection('usuarios').document(user.uid).set({
                'email': email,
                'role': role,  # ⚠️ IMPORTANTE: "role" no "rol"
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            return Response({
                "mensaje": "Usuario registrado correctamente",
                "uid": user.uid,
                "role": role
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Error al registrar: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

 
class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
 
        api_key = os.getenv('FIREBASE_WEB_API_KEY')

        if not email or not password:
            return Response(
                {"error": "Faltan credenciales"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not api_key:
            return Response(
                {"error": "Falta FIREBASE_WEB_API_KEY en el entorno"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
 
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            # ✅ Login correcto
            if response.status_code == 200:
                return Response({
                    "mensaje": "Login exitoso",
                    "token": data.get('idToken'),
                    "uid": data.get('localId')
                }, status=status.HTTP_200_OK)
 
            error_msg = data.get('error', {}).get('message', 'Error desconocido')

            return Response(
                {"error": error_msg},
                status=status.HTTP_401_UNAUTHORIZED
            )

        except Exception as e:
            return Response(
                {"error": f"Error en login: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )