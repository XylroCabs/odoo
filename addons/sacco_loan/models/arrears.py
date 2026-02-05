from odoo import models, fields, api
from datetime import date

class SaccoArrearsReport(models.Model):
    _name = 'sacco.arrears.report'
    _description = 'Loan Arrears Report'
    _auto = False  # computed model, not stored in DB

    member_id = fields.Many2one('res.partner', string="Member")
    loan_id = fields.Many2one('sacco.loan', string="Loan")
    due_date = fields.Date(string="Due Date")
    principal_amount = fields.Float(string="Principal")
    interest_amount = fields.Float(string="Interest")
    total_amount = fields.Float(string="Total")
    days_overdue = fields.Integer(string="Days Overdue")

    def init(self):
        """SQL view to compute arrears from repayment schedule"""
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW sacco_arrears_report AS (
                SELECT
                    line.id as id,
                    loan.member_id as member_id,
                    loan.id as loan_id,
                    line.due_date as due_date,
                    line.principal_amount as principal_amount,
                    line.interest_amount as interest_amount,
                    line.total_amount as total_amount,
                    (CURRENT_DATE - line.due_date) as days_overdue
                FROM sacco_repayment_schedule line
                JOIN sacco_loan loan ON line.loan_id = loan.id
                WHERE line.paid = FALSE AND line.due_date < CURRENT_DATE
            )
        """)
