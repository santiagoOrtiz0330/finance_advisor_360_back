# views.py
from rest_framework import generics
from ..models import Cliente, Demo
from ..serializers import ClienteSerializer
from ..serializers import DemoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils.openai_helper import generar_recomendaciones_financieras

# Vista para listar y crear clientes
class ClienteListCreateView(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# Vista para actualizar y eliminar clientes
class ClienteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class DemoCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DemoSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # # Generar sugerencia financiera
            # recomendaciones = generar_recomendaciones_financieras(serializer.data)

            # return Response({
            #     'data': serializer.data,
            #     'recomendaciones': recomendaciones
            # }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)