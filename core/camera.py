import cv2

class VideoCamera:
    def __init__(self):
        # Inicializar la cámara con cv2.VideoCapture(0)
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # Liberar correctamente la cámara cuando finalice su uso
        self.video.release()

    def get_frame(self):
        # Capturar frames continuamente (un frame a la vez)
        success, image = self.video.read()
        
        if not success:
            return None
            
        # Codificar cada frame en formato JPEG utilizando cv2.imencode()
        ret, jpeg = cv2.imencode('.jpg', image)
        
        if not ret:
            return None
            
        return jpeg.tobytes()
