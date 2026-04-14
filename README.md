# 📊 Sistema de Telemetría - API

## 📌 Descripción

Este proyecto consiste en una API REST desarrollada con **Django** y
**Django Rest Framework**, enfocada en la gestión de datos de
telemetría. Permite registrar, consultar y analizar información
proveniente de dispositivos en tiempo real.

## 🚀 Tecnologías usadas

-   Python
-   Django
-   Django Rest Framework
-   Firebase Firestore
-   Django Channels

## ⚙️ Funcionalidades principales

-   Registro de datos de telemetría
-   Autenticación de usuarios
-   Gestión de roles
-   Notificaciones en tiempo real
-   Historial de registros

## 🔐 Autenticación

El sistema utiliza autenticación basada en tokens y Firebase para
validar usuarios.

## 📡 Endpoints principales

-   `POST /api/telemetria/` → Registrar datos
-   `GET /api/telemetria/` → Listar datos
-   `GET /api/telemetria/{id}/` → Detalle específico

## 🧱 Arquitectura

El proyecto está dividido en múltiples aplicaciones Django: -
app_dashboard - app1 a app9

Cada módulo se encarga de una responsabilidad específica como usuarios,
datos, notificaciones, etc.

## 📂 Instalación

1.  Clonar el repositorio

2.  Crear entorno virtual

3.  Instalar dependencias:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Ejecutar migraciones:

    ``` bash
    python manage.py migrate
    ```

5.  Iniciar servidor:

    ``` bash
    python manage.py runserver
    ```

## 📈 Uso

Consumir la API mediante herramientas como Postman o desde el frontend
en Angular.

## 👨‍💻 Autor

Fabian David Torres
