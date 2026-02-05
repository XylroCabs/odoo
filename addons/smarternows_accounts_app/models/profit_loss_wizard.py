from odoo import models, fields

class ProfitLossWizard(models.TransientModel):
    _name = 'profit.loss.wizard'
    _description = 'Profit & Loss Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def get_profit_loss_lines(self):
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('move_id.state', '=', 'posted'),
            ('account_id.user_type_id.type', 'in', ['income', 'expense']),
        ]
        return self.env['account.move.line'].read_group(
            domain,
            ['debit:sum', 'credit:sum', 'balance:sum'],
            ['account_id']
        )

    def action_generate_profit_loss(self):
        data = {'lines': self.get_profit_loss_lines(),
                'date_from': self.date_from,
                'date_to': self.date_to}
        return self.env.ref('smarternows_accounts_app.action_report_profit_loss').report_action(None, data=data)
