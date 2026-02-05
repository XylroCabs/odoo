from odoo import models, fields

class TrialBalanceWizard(models.TransientModel):
    _name = 'trial.balance.wizard'
    _description = 'Trial Balance Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def action_generate_trial_balance(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'smarternows_accounts_app.trial_balance_template',
            'report_type': 'qweb-pdf',
            'context': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        }
