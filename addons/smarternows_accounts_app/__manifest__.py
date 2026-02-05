{
    'name': 'Smarternows Accounts App',
    'version': '1.0',
    'summary': 'Unified Accounting for Odoo Community v19',
    'description': """
        This module merges all business transactions (sales, purchases, bank, journal, assets)
        into a unified accounting view for easier reporting and management.
    """,
    'author': 'Jonathan Karimi Kiranga',
    'maintainer': 'Jonathan Karimi Kiranga',
    'website': 'https://smarternow-data-venture.odoo.com',  # replace with your actual site if different
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': ['base', 'account'],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views
        'views/account_merge_views.xml',
        'views/account_merge_menu.xml',
        'views/account_merge_ui.xml',
        'views/report_wizard.xml',
        'views/profit_loss_wizard.xml',
        'views/cash_flow_wizard.xml',
        'views/balance_sheet_wizard.xml',
        'views/asset_valuation_wizard.xml',
        'views/trial_balance_wizard.xml',
        'views/general_journal_views.xml',
        'views/general_journal_move_views.xml',
        'views/bank_ledger_views.xml',
        'views/bank_reconciliation_views.xml',

        # Reports
        'reports/reports.xml',
        'reports/profit_loss_template.xml',
        'reports/balance_sheet_template.xml',
        'reports/cash_flow_template.xml',
        'reports/asset_valuation_template.xml',
        'reports/trial_balance_template.xml',
        'reports/bank_reconciliation_template.xml',

        # Data
        'data/bank_journal.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
