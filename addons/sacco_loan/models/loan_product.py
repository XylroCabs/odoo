from odoo import models, fields

class SaccoLoanProduct(models.Model):
    _name = 'sacco.loan.product'
    _description = 'SACCO Loan Product'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    journal_id = fields.Many2one('account.journal', required=True)
    receivable_account_id = fields.Many2one('account.account', required=True)
    interest_income_account_id = fields.Many2one('account.account')
