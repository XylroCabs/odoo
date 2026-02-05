from odoo import models, fields

class CashFlowWizard(models.TransientModel):
    _name = 'cash.flow.wizard'
    _description = 'Cash Flow Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def get_cash_flow_lines(self):
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('move_id.state', '=', 'posted'),
            ('account_id.user_type_id.type', '=', 'liquidity'),
        ]
        return self.env['account.move.line'].read_group(
            domain,
            ['debit:sum', 'credit:sum', 'balance:sum'],
            ['account_id']
        )

    def action_generate_cash_flow(self):
        data = {'lines': self.get_cash_flow_lines(),
                'date_from': self.date_from,
                'date_to': self.date_to}
        return self.env.ref('smarternows_accounts_app.action_report_cash_flow').report_action(None, data=data)
