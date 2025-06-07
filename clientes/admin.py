from django.contrib import admin
from .models import Cliente, Demo, CompanyFinancials

class CompanyFinancialsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "language",
        "person_type",
        "full_name",
        "company_name",
        "industry",
        "state_of_residence",
        "cash_equivalents",
        "trade_receivables",
        "related_receivables",
        "inventories",
        "current_tax_assets",
        "bio_assets_fair",
        "bio_assets_cost",
        "other_fin_assets_curr",
        "other_nonfin_assets_curr",
        "total_curr_assets",

        "ppe",
        "inv_property",
        "goodwill",
        "other_intangibles",
        "bio_assets_noncurr",
        "equity_method_inv",
        "investments_assoc",
        "receivables_noncurr",
        "related_receivables_noncurr",
        "deferred_tax_assets",
        "tax_assets_noncurr",
        "other_fin_assets_noncurr",
        "other_nonfin_assets_noncurr",
        "total_non_curr_assets",

        "total_assets",

        "prov_curr",
        "acc_payable_curr",
        "related_payable_curr",
        "tax_liab_curr",
        "other_fin_liab_curr",
        "other_nonfin_liab_curr",
        "total_current_liabilities",

        "fin_liab_noncurr",
        "prov_noncurr",
        "acc_payable_noncurr",
        "deferred_tax_liab",
        "tax_liab_noncurr",
        "other_fin_liab_noncurr",
        "other_nonfin_liab_noncurr",
        "total_non_current_liabilities",

        "total_liabilities",

        "issued_capital",
        "share_premium",
        "treasury_shares",
        "reserves_total",
        "other_comprehensive_income",
        "other_equity_interests",
        "revaluation_surplus",
        "retained_earnings",
        "total_equity",
        "total_equity_liabilities",
    ]

#admin.site.register(Cliente)
#admin.site.register(Demo)
admin.site.register(CompanyFinancials, CompanyFinancialsAdmin)
