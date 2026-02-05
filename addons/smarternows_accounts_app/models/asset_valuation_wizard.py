from odoo import models, fields

class AssetValuationWizard(models.TransientModel):
    _name = 'asset.valuation.wizard'
    _description = 'Asset Valuation Wizard'

    date_to = fields.Date(string="End Date", required=True)

    def get_asset_valuation_lines(self):
        domain = [
            ('date', '<=', self.date_to),
            ('move_id.state', '=', 'posted'),
            ('account_id.user_type_id.type', '=', 'asset'),
        ]
        return self.env['account.move.line'].read_group(
            domain,
            ['debit:sum', 'credit:sum', 'balance:sum'],
            ['account_id']
        )

    def action_generate_asset_valuation(self):
        data = {'lines': self.get_asset_valuation_lines(),
                'date_to': self.date_to}
        return self.env.ref('smarternows_accounts_app.action_report_asset_valuation').report_action(None, data=data)
