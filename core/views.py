from django.shortcuts import render
from django.http import StreamingHttpResponse
from .camera import VideoCamera
from .models import Deteccion

def index(request):
    """
    Vista principal que renderiza el HTML donde se mostrará el video.
    Envía las estadísticas y últimas detecciones a la plantilla.
    """
    detecciones = Deteccion.objects.all().order_by('-fecha')[:5]
    total_detecciones = Deteccion.objects.count()
    ultima_deteccion = Deteccion.objects.order_by('-fecha').first()
    
    context = {
        'detecciones': detecciones,
        'total_detecciones': total_detecciones,
        'ultima_deteccion': ultima_deteccion,
    }
    return render(request, 'core/index.html', context)

def generate_frames(camera):
    """
    Función generadora que obtiene los frames de la cámara y 
    los formatea como partes de una respuesta multipart/x-mixed-replace.
    """
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    """
    Vista que devuelve un StreamingHttpResponse con los frames generados,
    utilizando el content-type multipart/x-mixed-replace.
    """
    return StreamingHttpResponse(
        generate_frames(VideoCamera()),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )
