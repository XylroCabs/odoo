
    'name': 'smarternow SACCO Loan Management',
    'version': '1.0',
    'summary': 'For Odoo v19.0 Loan products, applications, disbursements, and repayments with double-entry accounting',19
    'description': 'Manage SACCO loan products, member loans, repayments, and accounting integration with audit-ready reports.',
    'author': 'Your SACCO',
    'depends': ['base', 'account', 'contacts'],
    'data': [
    'security/ir.model.access.csv',
    'views/menu.xml',                # ✅ correct path
    'views/loan_product_views.xml',
    'views/loan_views.xml',
    'views/repayment_views.xml',
    'reports/loan_report.xml',
    'reports/member_statement_report.xml', # ✅ new report
    ],
    'installable': True,
    'application': True,
}

