import os
import pandas as pd
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from clientes.models import CompanyFinancials  # Importa tu modelo
from django.core.files.storage import default_storage

class ProcessExcelView(APIView):
    
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        filename = request.data.get('filename')
        if not filename:
            return Response({'error': 'Missing filename'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_storage.exists(filename):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            with default_storage.open(filename, 'rb') as f:
                df = pd.read_excel(f)

            expected_columns = 43
            if df.shape[1] != expected_columns:
                return Response({
                    'error': f'Incorrect number of columns. Expected {expected_columns}, got {df.shape[1]}'
                }, status=status.HTTP_400_BAD_REQUEST)

            df = df.where(pd.notnull(df), None)

            try:
                instance = CompanyFinancials.objects.get(pk=id)
            except CompanyFinancials.DoesNotExist:
                return Response({'error': 'Instance not found'}, status=status.HTTP_404_NOT_FOUND)

            # Solo procesamos la primera fila del archivo
            row = df.iloc[0]

            # Extrae los valores como antes
            instance.cash_equivalents = clean_value(row.iloc[0])
            instance.trade_receivables = clean_value(row.iloc[1])
            instance.related_receivables = clean_value(row.iloc[2])
            instance.inventories = clean_value(row.iloc[3])
            instance.current_tax_assets = clean_value(row.iloc[4])
            instance.bio_assets_fair = clean_value(row.iloc[5])
            instance.bio_assets_cost = clean_value(row.iloc[6])
            instance.other_fin_assets_curr = clean_value(row.iloc[7])
            instance.other_nonfin_assets_curr = clean_value(row.iloc[8])
            instance.total_curr_assets = (
                instance.cash_equivalents +
                instance.trade_receivables +
                instance.related_receivables +
                instance.inventories +
                instance.current_tax_assets +
                instance.bio_assets_fair +
                instance.bio_assets_cost +
                instance.other_fin_assets_curr +
                instance.other_nonfin_assets_curr
            )

            instance.ppe = clean_value(row.iloc[9])
            instance.inv_property = clean_value(row.iloc[10])
            instance.goodwill = clean_value(row.iloc[11])
            instance.other_intangibles = clean_value(row.iloc[12])
            instance.bio_assets_noncurr = clean_value(row.iloc[13])
            instance.equity_method_inv = clean_value(row.iloc[14])
            instance.investments_assoc = clean_value(row.iloc[15])
            instance.receivables_noncurr = clean_value(row.iloc[16])
            instance.related_receivables_noncurr = clean_value(row.iloc[17])
            instance.deferred_tax_assets = clean_value(row.iloc[18])
            instance.tax_assets_noncurr = clean_value(row.iloc[19])
            instance.other_fin_assets_noncurr = clean_value(row.iloc[20])
            instance.other_nonfin_assets_noncurr = clean_value(row.iloc[21])
            instance.total_non_curr_assets = (
                instance.ppe +
                instance.inv_property +
                instance.goodwill +
                instance.other_intangibles +
                instance.bio_assets_noncurr +
                instance.equity_method_inv +
                instance.investments_assoc +
                instance.receivables_noncurr +
                instance.related_receivables_noncurr +
                instance.deferred_tax_assets +
                instance.tax_assets_noncurr +
                instance.other_fin_assets_noncurr +
                instance.other_nonfin_assets_noncurr
            )

            instance.total_assets = instance.total_curr_assets + instance.total_non_curr_assets

            instance.prov_curr = clean_value(row.iloc[22])
            instance.acc_payable_curr = clean_value(row.iloc[23])
            instance.related_payable_curr = clean_value(row.iloc[24])
            instance.tax_liab_curr = clean_value(row.iloc[25])
            instance.other_fin_liab_curr = clean_value(row.iloc[26])
            instance.other_nonfin_liab_curr = clean_value(row.iloc[27])
            instance.total_current_liabilities = (
                instance.prov_curr +
                instance.acc_payable_curr +
                instance.related_payable_curr +
                instance.tax_liab_curr +
                instance.other_fin_liab_curr +
                instance.other_nonfin_liab_curr
            )

            instance.fin_liab_noncurr = clean_value(row.iloc[28])
            instance.prov_noncurr = clean_value(row.iloc[29])
            instance.acc_payable_noncurr = clean_value(row.iloc[30])
            instance.deferred_tax_liab = clean_value(row.iloc[31])
            instance.tax_liab_noncurr = clean_value(row.iloc[32])
            instance.other_fin_liab_noncurr = clean_value(row.iloc[33])
            instance.other_nonfin_liab_noncurr = clean_value(row.iloc[34])
            instance.total_non_current_liabilities = (
                instance.fin_liab_noncurr +
                instance.prov_noncurr +
                instance.acc_payable_noncurr +
                instance.deferred_tax_liab +
                instance.tax_liab_noncurr +
                instance.other_fin_liab_noncurr +
                instance.other_nonfin_liab_noncurr
            )

            instance.total_liabilities = instance.total_current_liabilities + instance.total_non_current_liabilities

            instance.issued_capital = clean_value(row.iloc[35])
            instance.share_premium = clean_value(row.iloc[36])
            instance.treasury_shares = clean_value(row.iloc[37])
            instance.reserves_total = clean_value(row.iloc[38])
            instance.other_comprehensive_income = clean_value(row.iloc[39])
            instance.other_equity_interests = clean_value(row.iloc[40])
            instance.revaluation_surplus = clean_value(row.iloc[41])
            instance.retained_earnings = clean_value(row.iloc[42])
            instance.total_equity = (
                instance.issued_capital +
                instance.share_premium +
                instance.treasury_shares +
                instance.reserves_total +
                instance.other_comprehensive_income +
                instance.other_equity_interests +
                instance.revaluation_surplus +
                instance.retained_earnings
            )
            instance.total_equity_liabilities = instance.total_equity + instance.total_liabilities

            instance.save()

            return Response({'message': 'Registro actualizado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Antes de guardar, limpia los valores 'nan' como string y np.nan
def clean_value(val):
    try:
        if pd.isna(val) or str(val).strip().lower() == 'nan':
            return 0.0
        return float(val)
    except (ValueError, TypeError):
        return 0.0