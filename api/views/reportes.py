from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from telemetria.firebase_config import db

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reporte_servidor(request, id_servidor):
    # CORRECCIÓN ESENCIAL: Limpieza de rol para evitar fallos por espacios o mayúsculas
    user_rol = str(getattr(request.user, 'rol', '')).strip().lower()
    
    if user_rol != "admin":
        return Response({"error": "Solo admins"}, status=403)

    docs = db.collection("telemetria")\
        .where("id_servidor", "==", id_servidor)\
        .stream()

    registros = [doc.to_dict() for doc in docs]

    if not registros:
        return Response({"error": "Sin datos"}, status=404)

    # CORRECCIÓN ESENCIAL: Evitar división por cero y asegurar tipos numéricos
    total_registros = len(registros)
    cpu_promedio = sum(float(r.get("cpu", 0)) for r in registros) / total_registros
    temp_maxima = max(float(r.get("temperatura", 0)) for r in registros)
    contador_anomalias = sum(1 for r in registros if r.get("anomalia") is True)

    return Response({
        "cpu_promedio": round(cpu_promedio, 2),
        "temp_maxima": temp_maxima,
        "contador_anomalias": contador_anomalias
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def estado_actual(request):
    # CORRECCIÓN ESENCIAL: Misma validación de rol que arriba
    user_rol = str(getattr(request.user, 'rol', '')).strip().lower()

    if user_rol != "admin":
        return Response({"error": "Solo admins"}, status=403)

    docs = db.collection("telemetria").stream()
    servidores = {}

    for doc in docs:
        data = doc.to_dict()
        srv = data.get("id_servidor")

        if not srv: 
            continue 

        if srv not in servidores:
            servidores[srv] = data
        else:
            t1 = data.get("timestamp")
            t2 = servidores[srv].get("timestamp")
            
            # CORRECCIÓN ESENCIAL: Manejo robusto de comparación de fechas
            if t1 and t2 and t1 > t2:
                servidores[srv] = data

    return Response(list(servidores.values()))