from odoo import models, fields

class BalanceSheetWizard(models.TransientModel):
    _name = 'balance.sheet.wizard'
    _description = 'Balance Sheet Wizard'

    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date", required=True)

    def get_balance_sheet_lines(self):
        domain = [
            ('date', '<=', self.date_to),
            ('move_id.state', '=', 'posted'),
            ('account_id.user_type_id.type', 'in', ['asset', 'liability', 'equity']),
        ]
        return self.env['account.move.line'].read_group(
            domain,
            ['debit:sum', 'credit:sum', 'balance:sum'],
            ['account_id']
        )

    def action_generate_balance_sheet(self):
        data = {'lines': self.get_balance_sheet_lines(),
                'date_from': self.date_from,
                'date_to': self.date_to}
        return self.env.ref('smarternows_accounts_app.action_report_balance_sheet').report_action(None, data=data)
