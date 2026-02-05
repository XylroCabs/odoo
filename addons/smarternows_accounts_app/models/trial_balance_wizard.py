from odoo import models, fields

class TrialBalanceWizard(models.TransientModel):
    _name = 'trial.balance.wizard'
    _description = 'Trial Balance Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def get_trial_balance_lines(self):
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('move_id.state', '=', 'posted'),
        ]
        return self.env['account.move.line'].read_group(
            domain,
            ['debit:sum', 'credit:sum', 'balance:sum'],
            ['account_id']
        )

    def action_generate_trial_balance(self):
        data = {'lines': self.get_trial_balance_lines(),
                'date_from': self.date_from,
                'date_to': self.date_to}
        return self.env.ref('smarternows_accounts_app.action_report_trial_balance').report_action(None, data=data)
