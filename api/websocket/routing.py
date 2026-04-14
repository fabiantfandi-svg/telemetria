from django.urls import path
from .consumers import AlertasConsumer

websocket_urlpatterns = [
    # Sin la barra al principio, con la barra al final
    path('ws/telemetria/', AlertasConsumer.as_asgi()),
]