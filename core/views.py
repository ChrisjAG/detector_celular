from django.shortcuts import render
from django.http import StreamingHttpResponse
from .camera import VideoCamera

def index(request):
    """
    Vista principal que renderiza el HTML donde se mostrará el video.
    """
    return render(request, 'core/index.html')

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
