import cv2
import time
import os
from django.conf import settings
from .models import Deteccion

class VideoCamera:
    def __init__(self):
        # Inicializar la cámara
        self.video = cv2.VideoCapture(0)
        
        # Rutas a los archivos del modelo YOLOv4-tiny
        base_dir = settings.BASE_DIR
        weights_path = os.path.join(base_dir, 'core', 'ml_models', 'yolov4-tiny.weights')
        cfg_path = os.path.join(base_dir, 'core', 'ml_models', 'yolov4-tiny.cfg')
        names_path = os.path.join(base_dir, 'core', 'ml_models', 'coco.names')
        
        # Intentar cargar el modelo si los archivos existen
        self.net = None
        self.classes = []
        self.output_layers = []
        
        if os.path.exists(weights_path) and os.path.exists(cfg_path) and os.path.exists(names_path):
            self.net = cv2.dnn.readNet(weights_path, cfg_path)
            # Usar backend predeterminado y CPU
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
            
            with open(names_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
            
            layer_names = self.net.getLayerNames()
            self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        
        # Variables para controlar el registro en la base de datos (Cooldown de 10 segundos)
        self.last_detection_time = 0
        self.cooldown_seconds = 10

    def __del__(self):
        # Liberar la cámara
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return None
            
        # Procesamiento de detección (solo si el modelo está cargado)
        if self.net:
            height, width, channels = frame.shape
            
            # Preparar el frame para la red neuronal
            blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)
            
            class_ids = []
            confidences = []
            boxes = []
            
            # Analizar las predicciones
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = scores.argmax()
                    confidence = scores[class_id]
                    
                    # Filtrar por confianza (> 50%) y clase ("cell phone", normalmente índice 67 en COCO)
                    if confidence > 0.5 and class_id < len(self.classes) and self.classes[class_id] == "cell phone":
                        # Coordenadas del bounding box
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            
            # Aplicar Non-Maximum Suppression para eliminar cajas duplicadas
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            
            celular_detectado = False
            
            if len(indexes) > 0:
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    confidence = confidences[i]
                    
                    # Dibujar bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # Mostrar texto y porcentaje
                    label = f"Celular: {confidence:.2f}"
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    celular_detectado = True
            
            # Registrar en PostgreSQL si se detectó un celular y pasó el cooldown
            current_time = time.time()
            if celular_detectado and (current_time - self.last_detection_time) > self.cooldown_seconds:
                Deteccion.objects.create(objeto_detectado="Celular")
                self.last_detection_time = current_time
        else:
            # Si el modelo no está cargado, mostrar una advertencia en el video
            cv2.putText(frame, "Modelo YOLOv4-tiny no encontrado", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Codificar en JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None
            
        return jpeg.tobytes()
