from django.urls import path
from .views.ingesta import ingesta
from .views.reportes import reporte_servidor, estado_actual
from .views_auth import RegistroAPIView, LoginApiView

urlpatterns = [
    path('telemetria/ingesta/', ingesta),
    path('telemetria/reporte/<str:id_servidor>/', reporte_servidor),
    path('telemetria/estado-actual/', estado_actual),

    
    path('registro/', RegistroAPIView.as_view()),
    path('login/', LoginApiView.as_view()),
]