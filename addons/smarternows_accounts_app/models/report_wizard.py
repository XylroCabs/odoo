from odoo import models, fields

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Generic Report Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)

    def action_generate_report(self):
        return {
            'type': 'ir.actions.report',
            'report_name': 'smarternows_accounts_app.cash_flow_template',
            'report_type': 'qweb-pdf',
            'context': {
                'date_from': self.date_from,
                'date_to': self.date_to,
            }
        }
