# serializers.py
from rest_framework import serializers
from .models import Cliente, Demo, CompanyFinancials

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'correo', 'telefono']

class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demo
        fields = '__all__'

class CompanyFinancialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFinancials
        fields = '__all__'


# Serializers define the API representation.
class UploadSerializer(serializers.Serializer):
    '''
    UploadSerializer Serializador para la subida de archivos
    '''
    file_uploaded = serializers.FileField()
    class Meta:
        '''
        Redefinición de clase padre para serializar el archivo
        '''
        fields = ['file_uploaded']