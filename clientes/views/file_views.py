'''
Archivo para los views de los carga de archivos ApiFallecidos
'''
import os
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from clientes.serializers import UploadSerializer


class FileUploadView(ViewSet):
    '''
    Sube al servidor los archivos adjuntos en la petición
    '''
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer

    def create(self, request):
        '''
        Permite subir al servidor archivos
        '''

        file_uploaded = request.FILES.get('file_uploaded')

        if not file_uploaded:
            raise ParseError("Sin archivo adjunto")

        _, file_extension = os.path.splitext(str(file_uploaded))

        username = request.user.get_username().split('@')[0].upper()
        date = str(
            datetime.now()
        ).replace(' ', '_').replace('.', '_').replace(':', '').replace('-', '')

        filename = f'{username}_{date}{file_extension}'

        default_storage.save(
            str(filename), ContentFile(file_uploaded.read()))


        return Response({
            'count': 0,
            'next': None,
            'previous': None,
            'stop': False,
            'message': 'El archivo fue guardado exitosamente',
            'results': {
                'NOMBRE_SISTEMA': filename
            },
        }, status.HTTP_201_CREATED)

