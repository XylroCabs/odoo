from odoo import models, fields

class AssetValuationWizard(models.TransientModel):
    _name = 'asset.valuation.wizard'
    _description = 'Asset Valuation Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def action_generate_asset_valuation(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'smarternows_accounts_app.asset_valuation_template',
            'report_type': 'qweb-pdf',
            'context': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        }
