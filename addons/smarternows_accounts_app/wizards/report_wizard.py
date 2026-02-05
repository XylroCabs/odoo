from odoo import models, fields

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Report Wizard'

    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")

