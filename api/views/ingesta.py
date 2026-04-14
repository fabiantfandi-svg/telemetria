from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from telemetria.firebase_config import db
from firebase_admin import firestore
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ingesta(request):

    # CORRECCIÓN: Usamos .rol (notación de objeto) en lugar de ["role"]
    if request.user.rol != "sensor":
        return Response({"error": "Solo sensores"}, status=403)

    data = request.data

    cpu = data.get("cpu", 0)
    temperatura = data.get("temperatura", 0)

    anomalia = cpu > 90 or temperatura > 75

    # Guardar en Firestore
    db.collection("telemetria").add({
        "id_servidor": data.get("id_servidor"),
        "cpu": cpu,
        "ram": data.get("ram"),
        "temperatura": temperatura,
        "anomalia": anomalia,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    if anomalia:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "alertas",
            {
                "type": "enviar_alerta",
                "data": {
                    "alerta": "CRÍTICA",
                    "servidor": data.get("id_servidor"),
                    "motivo": f"CPU: {cpu}% o Temp: {temperatura}°C elevados"
                }
            }
        )

    return Response({"anomalia": anomalia}, status=201)