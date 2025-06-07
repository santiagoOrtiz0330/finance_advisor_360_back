# urls.py
from django.urls import path
from django.urls.conf import include
from .views.views import ClienteListCreateView, ClienteRetrieveUpdateDestroyView, DemoCreateView
from clientes.views.file_views import FileUploadView
from clientes.views.financial_analysis import FinancialAnalysisView
from clientes.views.company_financial_view import CompanyFinancialsCreateView
from rest_framework import routers
from clientes.views.masive import ProcessExcelView

router = routers.DefaultRouter()

router.register(
    r'file_upload',
    FileUploadView,
    basename='file_upload'
)

urlpatterns = [
    path(
        '', include(router.urls)),
    path('clientes/demo/', DemoCreateView.as_view(), name='demo-create'),
    path('clientes/company_create/', CompanyFinancialsCreateView.as_view(), name='company-create'),
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<int:pk>/', ClienteRetrieveUpdateDestroyView.as_view(), name='cliente-retrieve-update-destroy'),
    path('clientes/masive/<int:id>/', ProcessExcelView.as_view(), name='masive-excel'),
    path('clientes/financial_analysis/<int:id>/', FinancialAnalysisView.as_view(), name='financial-analysis'),
]