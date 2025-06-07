# views.py
from clientes.models import CompanyFinancials
from ..serializers import CompanyFinancialsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..utils.openai_helper import generar_recomendaciones_financieras




class CompanyFinancialsCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CompanyFinancialsSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            return Response({
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)