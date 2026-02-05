from odoo import models, fields

class BalanceSheetWizard(models.TransientModel):
    _name = 'balance.sheet.wizard'
    _description = 'Balance Sheet Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def action_generate_balance_sheet(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'smarternows_accounts_app.balance_sheet_template',
            'report_type': 'qweb-pdf',
            'context': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        }
