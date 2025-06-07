import openai
from django.conf import settings
from mi_crud_project.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generar_recomendaciones_financieras(datos):
    prompt = f"""
Eres un asesor financiero experto. Un cliente te ha proporcionado la siguiente información financiera:

- Tipo de persona: {datos.get('person_type')}
- Nombre: {datos.get('full_name') or datos.get('company_name')}
- Edad: {datos.get('age', 'N/A')}
- Estado de residencia: {datos.get('state_of_residence')}

Ingresos y activos:
- Ingreso mensual: {datos.get('monthly_income')}
- Efectivo disponible: {datos.get('cash')}
- Inversiones: {datos.get('investments')}
- Bienes raíces: {datos.get('real_estate')}
- Otros activos: {datos.get('other_assets')}

Pasivos:
- Préstamos: {datos.get('loans')}
- Deuda en tarjeta de crédito: {datos.get('credit_card_debt')}
- Otras obligaciones: {datos.get('other_liabilities')}

Con base en esta información, proporciona 3 sugerencias financieras personalizadas y prácticas para mejorar su salud financiera. Explica cada sugerencia brevemente.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asesor financiero experto."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=6000
    )

    return response['choices'][0]['message']['content']
