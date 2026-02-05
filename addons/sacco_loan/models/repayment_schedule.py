from odoo import models, fields, api

class SaccoRepaymentSchedule(models.Model):
    _name = 'sacco.repayment.schedule'
    _description = 'Loan Repayment Schedule'

    loan_id = fields.Many2one('sacco.loan', required=True)
    due_date = fields.Date(required=True)
    principal_amount = fields.Float(required=True)
    interest_amount = fields.Float(required=True)
    total_amount = fields.Float(compute="_compute_total", store=True)
    paid = fields.Boolean(default=False)

    @api.depends('principal_amount', 'interest_amount')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = rec.principal_amount + rec.interest_amount
