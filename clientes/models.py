from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre



class Demo(models.Model):
    PERSON_TYPE_CHOICES = [
        ('Person', 'Person'),
        ('Company', 'Company'),
    ]

    person_type = models.CharField(
        max_length=10,
        choices=PERSON_TYPE_CHOICES,
        verbose_name='Type of Person'
    )

    # Shared / Person fields
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    state_of_residence = models.CharField(max_length=100)

    # Company-specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    number_of_employees = models.PositiveIntegerField(blank=True, null=True)
    annual_revenue = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)

    # Shared financial fields
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cash = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    investments = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    real_estate = models.DecimalField(max_digits=12, decimal_places=2,blank=True, null=True)
    other_assets = models.DecimalField(max_digits=12, decimal_places=2)

    loans = models.DecimalField(max_digits=12, decimal_places=2)
    credit_card_debt = models.DecimalField(max_digits=12, decimal_places=2)
    other_liabilities = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name if self.person_type == 'Company' else self.full_name
    

class CompanyFinancials(models.Model):
    
    PERSON_TYPE_CHOICES = [
        ('Person', 'Person'),
        ('Company', 'Company'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Español'),
    ]

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en', 
    )

    person_type = models.CharField(
        max_length=10,
        choices=PERSON_TYPE_CHOICES,
        verbose_name='Type of Person'
    )

    # Shared / Person fields
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    state_of_residence = models.CharField(max_length=100, blank=True, null=True)

    # Company-specific fields
    company_name = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)

    cash_equivalents = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Efectivo y equivalentes al efectivo

    trade_receivables = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas comerciales por cobrar

    related_receivables = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas por cobrar partes relacionadas

    inventories = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Inventarios

    current_tax_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos por impuestos corrientes

    bio_assets_fair = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos biológicos corrientes al valor razonable

    bio_assets_cost = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos biológicos corrientes al costo menos depreciación y deterioro

    other_fin_assets_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros activos financieros corrientes

    other_nonfin_assets_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros activos no financieros corrientes

    # Activos corrientes totales
    total_curr_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    ppe = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Propiedad, planta y equipo

    inv_property = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Propiedad de inversión

    goodwill = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Plusvalía

    other_intangibles = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos intangibles distintos de la plusvalía

    bio_assets_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos biológicos no corrientes

    equity_method_inv = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Inversiones contabilizadas utilizando el método de la participación

    investments_assoc = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Inversiones en subsidiarias, negocios conjuntos y asociadas

    receivables_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas por cobrar no corrientes

    related_receivables_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas por cobrar partes relacionadas

    deferred_tax_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos por impuestos diferidos

    tax_assets_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Activos por impuestos no corrientes

    other_fin_assets_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros activos financieros no corrientes

    other_nonfin_assets_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros activos no financieros no corrientes

    total_non_curr_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de activos no corrientes

    total_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total activos

    prov_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de provisiones corrientes

    acc_payable_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas por pagar corrientes

    related_payable_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas por cobrar partes relacionadas

    tax_liab_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Pasivos por impuestos corrientes

    other_fin_liab_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros pasivos financieros corrientes

    other_nonfin_liab_curr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros pasivos no financieros corrientes

    total_current_liabilities = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de pasivo corriente

    fin_liab_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Pasivos financieros no corrientes

    prov_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de provisiones no corrientes

    acc_payable_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Cuentas por pagar no corrientes

    deferred_tax_liab = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Pasivo por impuestos diferidos

    tax_liab_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Pasivos por impuestos no corrientes

    other_fin_liab_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros pasivos financieros no corrientes

    other_nonfin_liab_noncurr = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otros pasivos no financieros no corrientes

    total_non_current_liabilities= models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de pasivos no corrientes

    total_liabilities= models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total Pasivos

    issued_capital = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Capital emitido

    share_premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Prima de emisión

    treasury_shares = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Acciones propias readquiridas

    reserves_total = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de reservas

    other_comprehensive_income = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otro resultado integral

    other_equity_interests = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Otras participaciones en el patrimonio

    revaluation_surplus = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Superávit por revaluación

    retained_earnings = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Ganancias acumuladas

    total_equity = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Patrimonio total

    total_equity_liabilities = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    # Total de patrimonio y pasivos

    gpt_prompt = models.TextField(null=True, blank=True)
    # Promp enviado a ChatGPT

    gpt_response = models.TextField(null=True, blank=True)
    # Sugerencias que responde ChatGPT

    class Meta:
        verbose_name_plural = 'Company Financials'