from odoo import models, fields

class ProfitLossWizard(models.TransientModel):
    _name = 'profit.loss.wizard'
    _description = 'Profit & Loss Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def action_generate_profit_loss(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'smarternows_accounts_app.profit_loss_template',
            'report_type': 'qweb-pdf',
            'context': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        }

