# Detector Celular con IA

Este es un proyecto web desarrollado con Django y OpenCV para la detección y transmisión de video en tiempo real desde una cámara web. Utiliza inteligencia artificial (YOLOv4-tiny) para detectar teléfonos celulares. La interfaz está construida con un diseño premium y moderno, y los registros se almacenan en una base de datos PostgreSQL.

## Capturas de Pantalla

![Interfaz Principal](ruta/a/tu/captura1.png "Marcador de posición para captura de la interfaz")
![Detección en tiempo real](ruta/a/tu/captura2.png "Marcador de posición para captura de detección de celular")
![Historial de Detecciones](ruta/a/tu/captura3.png "Marcador de posición para la tabla de últimas detecciones")

## Requisitos

- Python 3.8+
- PostgreSQL
- Cámara web funcional

## 1. Configuración de PostgreSQL

Asegúrate de tener un servidor PostgreSQL ejecutándose. Puedes configurar la conexión mediante variables de entorno (o editando los valores por defecto en `detector_celular/settings.py`):

Crea la base de datos en PostgreSQL antes de ejecutar las migraciones:
```sql
CREATE DATABASE detector_celular_db;
```

Variables de entorno configurables:
- `DB_ENGINE`: Motor de base de datos (por defecto: `django.db.backends.postgresql`)
- `DB_NAME`: Nombre de la base de datos (por defecto: `detector_celular_db`)
- `DB_USER`: Usuario de la base de datos (por defecto: `postgres`)
- `DB_PASSWORD`: Contraseña (por defecto: `postgres`)
- `DB_HOST`: Host de la base de datos (por defecto: `localhost`)
- `DB_PORT`: Puerto de la base de datos (por defecto: `5432`)

## 2. Descargar el Modelo de Detección (YOLOv4-tiny)

El sistema utiliza el modelo YOLOv4-tiny pre-entrenado en el dataset COCO. Debes descargar 3 archivos y colocarlos en la carpeta `core/ml_models/` de tu proyecto (crea la carpeta si no existe):

1. **Pesos (`yolov4-tiny.weights`):** [Descargar aquí](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights)
2. **Configuración (`yolov4-tiny.cfg`):** [Descargar aquí](https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg)
3. **Nombres de clases (`coco.names`):** [Descargar aquí](https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names)

> Nota: El archivo `coco.names` debe contener la clase "cell phone" (usualmente en la línea 68).

## 3. Instalación y Ejecución

Sigue estos comandos en tu terminal para configurar el proyecto:

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Crear y aplicar migraciones a PostgreSQL:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

## 4. Cómo Probar el Sistema

Para verificar que todo funciona correctamente (Casos de Prueba):

1. **Prueba de Streaming:** Abre el navegador e ingresa a `http://127.0.0.1:8000/`. Debes ver la interfaz moderna con el título "Detector de Celulares" y el video en vivo de tu cámara. Si ves el badge animado de "Cámara activa", el streaming funciona.
2. **Prueba de Detección:** Coloca un teléfono celular frente a tu cámara web. Debería aparecer un recuadro verde (bounding box) alrededor del celular con el texto "Celular" y su porcentaje de confianza.
3. **Prueba de Almacenamiento PostgreSQL:** Mientras sostienes el celular, el sistema guardará un registro (cada 10 segundos para evitar spam). Recarga la página y revisa la sección "Últimas detecciones".
4. **Prueba de Historial (Tabla):** En la tabla inferior deberás ver reflejada la fecha, la hora exacta y el objeto detectado ("Celular"). Si quitas el celular de la cámara por más de 10 segundos y lo vuelves a poner, verás un nuevo registro aparecer al recargar la página. Si eliminas todas las detecciones de la base de datos (o la instalas desde cero), la tabla mostrará correctamente el estado vacío: "No existen detecciones registradas."
