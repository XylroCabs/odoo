from odoo import models, fields

class ProfitLossWizard(models.TransientModel):
    _name = 'profit.loss.wizard'
    _description = 'Profit & Loss Wizard'

    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
