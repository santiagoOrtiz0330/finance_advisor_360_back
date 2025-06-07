import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from clientes.models import CompanyFinancials
from django.forms.models import model_to_dict
from decimal import Decimal
from mi_crud_project.settings import OPENAI_API_KEY
import os

# 611788990 - 20Joseluis
# Configura API Key de OpenAI
openai.api_key = OPENAI_API_KEY

class FinancialAnalysisView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')

        if not id:
            return Response({'error': 'ID not provided'}, status=400)

        try:
            financial = CompanyFinancials.objects.get(pk=id)
        except CompanyFinancials.DoesNotExist:
            return Response({'error': 'Financial record not found'}, status=404)


        # Diccionario de campo: descripción amigable
        field_descriptions = {
            "cash_equivalents": "Efectivo y equivalentes al efectivo",
            "trade_receivables": "Cuentas comerciales por cobrar",
            "related_receivables": "Cuentas por cobrar partes relacionadas",
            "inventories": "Inventarios",
            "current_tax_assets": "Activos por impuestos corrientes",
            "bio_assets_fair": "Activos biológicos corrientes al valor razonable",
            "bio_assets_cost": "Activos biológicos corrientes al costo menos depreciación y deterioro",
            "other_fin_assets_curr": "Otros activos financieros corrientes",
            "other_nonfin_assets_curr": "Otros activos no financieros corrientes",
            "total_curr_assets": "Total de activos corrientes",
            "ppe": "Propiedad, planta y equipo",
            "inv_property": "Propiedad de inversión",
            "goodwill": "Plusvalía",
            "other_intangibles": "Activos intangibles distintos de la plusvalía",
            "bio_assets_noncurr": "Activos biológicos no corrientes",
            "equity_method_inv": "Inversiones por método de participación",
            "investments_assoc": "Inversiones en subsidiarias, negocios conjuntos y asociadas",
            "receivables_noncurr": "Cuentas por cobrar no corrientes",
            "related_receivables_noncurr": "Cuentas por cobrar partes relacionadas (no corrientes)",
            "deferred_tax_assets": "Activos por impuestos diferidos",
            "tax_assets_noncurr": "Activos por impuestos no corrientes",
            "other_fin_assets_noncurr": "Otros activos financieros no corrientes",
            "other_nonfin_assets_noncurr": "Otros activos no financieros no corrientes",
            "total_non_curr_assets": "Total de activos no corrientes",
            "total_assets": "Total de activos",
            "prov_curr": "Provisiones corrientes",
            "acc_payable_curr": "Cuentas por pagar corrientes",
            "related_payable_curr": "Cuentas por pagar partes relacionadas",
            "tax_liab_curr": "Pasivos por impuestos corrientes",
            "other_fin_liab_curr": "Otros pasivos financieros corrientes",
            "other_nonfin_liab_curr": "Otros pasivos no financieros corrientes",
            "total_current_liabilities": "Total de pasivos corrientes",
            "fin_liab_noncurr": "Pasivos financieros no corrientes",
            "prov_noncurr": "Provisiones no corrientes",
            "acc_payable_noncurr": "Cuentas por pagar no corrientes",
            "deferred_tax_liab": "Pasivos por impuestos diferidos",
            "tax_liab_noncurr": "Pasivos por impuestos no corrientes",
            "other_fin_liab_noncurr": "Otros pasivos financieros no corrientes",
            "other_nonfin_liab_noncurr": "Otros pasivos no financieros no corrientes",
            "total_non_current_liabilities": "Total de pasivos no corrientes",
            "total_liabilities": "Total de pasivos",
            "issued_capital": "Capital emitido",
            "share_premium": "Prima de emisión",
            "treasury_shares": "Acciones propias readquiridas",
            "reserves_total": "Total de reservas",
            "other_comprehensive_income": "Otro resultado integral",
            "other_equity_interests": "Otras participaciones en el patrimonio",
            "revaluation_surplus": "Superávit por revaluación",
            "retained_earnings": "Ganancias acumuladas",
            "total_equity": "Total del patrimonio",
            "total_equity_liabilities": "Total de patrimonio y pasivos"
        }

        # Convertir modelo a dict y limpiar valores None
        data = model_to_dict(financial)
        financial_lines = [
            f"- {field_descriptions.get(key, key)}: {float(value):,.2f}"
            for key, value in data.items()
            if value is not None and isinstance(value, Decimal)
        ]

        financial_summary = "\n".join(financial_lines)

        # Configurar idioma
        if financial.language == "es":
            lang_instructions = (
                "Responde completamente en español. Usa un lenguaje simple, claro y humano, "
                "sin tecnicismos innecesarios. El tono debe ser empático, directo y motivador."
            )
        else:
            lang_instructions = (
                "Respond entirely in English. Use plain, simple and human language, "
                "without unnecessary technicalities. The tone must be empathetic, clear, and motivational."
            )

        # Rol del asesor según tipo de cliente
        if financial.person_type == 'Company':
            client_type = "una empresa"
            industry = f"en el sector {financial.person_type}"
        else: 
            client_type = "una persona"
            industry=''
        country = financial.state_of_residence

        # Prompt final
        # prompt = f"""
        #     Actúa como un asesor financiero experto.

        #     Estoy compartiendo el estado financiero de una empresa del sector comercial en Colombia.
        #     El objetivo es recibir recomendaciones para mejorar su rentabilidad, liquidez y eficiencia en el uso de sus recursos.

        #     Aquí están los datos financieros clave:

        #     {financial_summary}

        #     Con base en esta información:
        #     - Analiza la estructura financiera de la empresa.
        #     - Evalúa la liquidez, solvencia y rentabilidad.
        #     - Dame recomendaciones prácticas para mejorar su situación financiera.
        #     - Sugiere oportunidades de inversión, reducción de pasivos o crecimiento.
        #     """

        # Llamada a la API de OpenAI
        # response = openai.ChatCompletion.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": "Actúa como un asesor financiero experto."},
        #         {"role": "user", "content": prompt}
        #     ]
        # )

        content=f"""
            Actúa como un asesor experto en finanzas personales y corporativas que ha sido contratado por Protax,
            una plataforma digital especializada en diagnóstico financiero y recomendaciones personalizadas para clientes 
            latinos en EE. UU. y América Latina. Tu rol es analizar los datos financieros de {client_type} que opera en {country} {industry}
            (balance general, activos, pasivos, patrimonio, etc.), y a partir de ese análisis, brindar un feedback personalizado, 
            práctico y empático.
            {lang_instructions}
            Organiza el feedback en subtítulos, incluyendo: estructura financiera, liquidez, solvencia y recomendaciones prácticas.
            Tu objetivo es ayudar al usuario a entender su situación financiera y ofrecerle acciones concretas para mejorarla.
        """
        prompt = f"""
            Estos son los datos financieros más recientes:

            {financial_summary}

            Por favor, realiza un diagnóstico financiero estructurado siguiendo el enfoque de Protax.
        """

        # Llamada a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": (content)
                },
                {   
                    "role": "user", 
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message["content"]
        # result = 'Primero, vamos a analizar la estructura financiera de esta empresa.\n\nLa estructura financiera depende de cómo se financian los activos de la empresa. Los activos totales de la empresa son aproximadamente 1,955,136,056.00 y se financian tanto con deuda (pasivos que suman 1,333,581,556.00) como con capital propio (patrimonio de 621,554,500.00). Esto significa que la empresa está financiada aproximadamente al 68.2% con fondos prestados y el 31.8% restante con fondos propios. Debe tenerse en cuenta que una estructura financiera con alto nivel de deuda puede ser riesgosa y, a largo plazo, se debe buscar un equilibrio financiero mejor.\n\nEn términos de liquidez, la empresa parece tener suficientes activos corrientes (363,414,056.00) para cubrir sus pasivos corrientes (497,327,500.00), aunque la relación activo corriente / pasivo corriente de 0.73 indica que la empresa puede tener dificultades para cumplir con sus obligaciones a corto plazo. \n\nLa solvencia, que considera tanto los pasivos corrientes como no corrientes, parece saludable con una relación de activo total / deuda total de aproximadamente 1.47, lo que indica que la empresa tiene más activos que deudas. Sin embargo, gran parte de esta solvencia proviene de activos no corrientes.\n\nEn cuanto a la rentabilidad, no tenemos suficiente información para hacer una evaluación adecuada. Sería útil conocer las ganancias antes de intereses, impuestos, depreciación y amortización (EBITDA), y por supuesto, las ventas netas.\n\nAhora, algunas recomendaciones para mejorar la situación financiera de la empresa:\n\n1. Reducir la Deuda: Dado que la empresa tiene una cantidad significativa de deuda, podría dirigir un mayor porcentaje de sus ganancias futuras hacia la reducción de la deuda. Aunque el endeudamiento puede ser un instrumento útil para financiar operaciones y crecimiento, un nivel de endeudamiento demasiado elevado puede llevar al colapso financiero.\n\n2. Mejorar la gestión del capital de trabajo: La empresa puede buscar optimizar su gestión del capital de trabajo. Por ejemplo, puede tratar de acelerar las cobranzas (cuentas por cobrar) para mejorar su liquidez. También puede considerar maneras de reducir los niveles de inventario sin comprometer las ventas.\n\n3. Inversiones Inteligentes: Dado que la empresa tiene un monto considerable en propiedades, planta y equipo, podría explorar oportunidades para maximizar su rentabilidad, apalancando estos activos, posiblemente a través de la digitalización, modernización o la optimización de sus procesos y operaciones.\n\nDe igual manera, dada la situación de la empresa, podría ser prudente pausar o disminuir temporalmente cualquier expansión significativa hasta que su flujo de efectivo operativo mejore y los niveles de deuda se reduzcan.'

        # Guardar resultado en el modelo
        financial.gpt_prompt = f"{content}\n{prompt} "
        financial.gpt_response = result
        financial.save()


        return Response({"recomendaciones": result})
