{
    'name': 'Smarternows Accounts App',
    'version': '1.0',
    'summary': 'Unified Accounting for Odoo Community v19',
    'description': """
        This module merges all business transactions (sales, purchases, bank, journal, assets)
        into a unified accounting view for easier reporting and management.
    """,
    'author': 'Jonathan Karimi Kiranga',
    'category': 'Accounting',
    'depends': ['sale', 'purchase', 'account', 'account_asset'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_merge_views.xml',
        'views/account_merge_menu.xml',
        'views/account_merge_ui.xml',
        'views/report_wizard.xml',
        'views/profit_loss_wizard.xml',
        'reports/profit_loss_report.xml',
        'reports/profit_loss_template.xml',
        'reports/cash_flow_report.xml',
        'reports/cash_flow_template.xml',
        'reports/asset_valuation_report.xml',
        'reports/asset_valuation_template.xml',
        'reports/balance_sheet_report.xml',
        'reports/balance_sheet_template.xml',
    ],
    'installable': True,
    'application': True,
}
