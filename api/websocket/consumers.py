from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AlertasConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = "alertas" # Definirlo como atributo es una buena práctica

        # Unirse al grupo de alertas
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Aceptar la conexión
        await self.accept()

    async def disconnect(self, close_code):
        # Salir del grupo al desconectarse
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Este método se activa cuando envías algo desde fuera (ej. una vista)
    async def enviar_alerta(self, event):
        # Asegúrate de enviar solo la parte de los datos
        mensaje = event.get("data", event) 
        
        await self.send(text_data=json.dumps({
            "type": "alerta_critica",
            "payload": mensaje
        }))