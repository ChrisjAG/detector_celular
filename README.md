<<<<<<< HEAD
# detector_celular
=======
# Detector Celular

Este es un proyecto web desarrollado con Django y OpenCV para la detección y transmisión de video en tiempo real desde una cámara web. Utiliza PostgreSQL como base de datos para almacenar registros de detecciones. El streaming de video se realiza a través de HTTP (`StreamingHttpResponse` usando `multipart/x-mixed-replace`), lo que permite visualizar el video en el navegador sin utilizar JavaScript o WebSockets.

## Requisitos

- Python 3.8+
- PostgreSQL
- Cámara web funcional

## Estructura del Proyecto

```text
Detector_Celular/
│
├── core/                       # Aplicación principal
│   ├── templates/core/         # Plantillas HTML
│   │   └── index.html          # Vista principal con el reproductor de video
│   ├── __init__.py
│   ├── admin.py                # Registro del modelo Deteccion
│   ├── apps.py                 # Configuración de la app
│   ├── camera.py               # Lógica de captura y codificación con OpenCV
│   ├── models.py               # Definición del modelo Deteccion
│   ├── urls.py                 # Rutas específicas de la aplicación core
│   └── views.py                # Controladores, incluyendo el generador de video
│
├── detector_celular/           # Configuración del proyecto Django
│   ├── __init__.py
│   ├── asgi.py                 # Configuración ASGI (no usado para WebSockets aquí)
│   ├── settings.py             # Configuración general y de PostgreSQL
│   ├── urls.py                 # Rutas principales
│   └── wsgi.py                 # Configuración WSGI
│
├── .gitignore                  # Archivos ignorados por Git
├── manage.py                   # Script de gestión de Django
├── README.md                   # Documentación del proyecto
└── requirements.txt            # Dependencias del proyecto
```

## Configuración de PostgreSQL

Asegúrate de tener un servidor PostgreSQL ejecutándose. Puedes configurar la conexión mediante variables de entorno (o editando los valores por defecto en `detector_celular/settings.py`):

- `DB_ENGINE`: Motor de base de datos (por defecto: `django.db.backends.postgresql`)
- `DB_NAME`: Nombre de la base de datos (por defecto: `detector_celular_db`)
- `DB_USER`: Usuario de la base de datos (por defecto: `postgres`)
- `DB_PASSWORD`: Contraseña (por defecto: `postgres`)
- `DB_HOST`: Host de la base de datos (por defecto: `localhost`)
- `DB_PORT`: Puerto de la base de datos (por defecto: `5432`)

Crea la base de datos en PostgreSQL antes de ejecutar las migraciones:
```sql
CREATE DATABASE detector_celular_db;
```

## Instalación y Ejecución

Sigue estos comandos en tu terminal para configurar el proyecto en Windows (PowerShell/CMD):

1. **Crear el entorno virtual:**
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual:**
   - En Windows (PowerShell/CMD):
     ```bash
     .\venv\Scripts\activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crear migraciones:**
   ```bash
   python manage.py makemigrations core
   ```

5. **Ejecutar migrate:**
   ```bash
   python manage.py migrate
   ```

6. **Crear un superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor:**
   ```bash
   python manage.py runserver
   ```

Abre tu navegador y accede a `http://127.0.0.1:8000/`. Podrás ver la transmisión de la cámara web.
Puedes acceder al panel de administración en `http://127.0.0.1:8000/admin/` para gestionar los registros de Deteccion.

## Función de cada archivo generado

- **requirements.txt**: Define las librerías de Python requeridas (`Django`, `psycopg2-binary`, `opencv-python`).
- **.gitignore**: Evita que archivos innecesarios como el entorno virtual y la caché se suban al control de versiones.
- **settings.py**: Archivo principal de configuración de Django, configurado con PostgreSQL.
- **urls.py (Proyecto)**: Enruta las peticiones de la raíz hacia la aplicación `core`.
- **models.py**: Define la estructura de la base de datos (`Deteccion`).
- **admin.py**: Configura qué modelos pueden ser gestionados por los administradores en `/admin/`.
- **camera.py**: Encapsula la lógica de OpenCV en la clase `VideoCamera` para capturar y codificar frames en JPEG.
- **views.py**: Contiene las vistas `index` (para renderizar la interfaz) y `video_feed` (para gestionar la respuesta de streaming HTTP continua).
- **urls.py (App core)**: Mapea las URLs específicas como la raíz y `/video_feed/` hacia sus respectivas vistas.
- **index.html**: Plantilla base utilizando Bootstrap 5 que incluye la etiqueta `<img>` para recibir el stream de video.
>>>>>>> 87b60be (Proyecto detector celular - Sesion 1 funcionando)
