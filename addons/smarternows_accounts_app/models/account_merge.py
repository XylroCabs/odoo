from odoo import models, fields

class AccountMerge(models.Model):
    _name = 'account.merge'
    _description = 'Unified Accounting Transactions'

    name = fields.Char(string="Transaction Reference")
    date = fields.Date(string="Date")
    partner_id = fields.Many2one('res.partner', string="Partner")
    transaction_type = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('bank', 'Bank'),
        ('journal', 'Journal'),
        ('asset', 'Asset'),
    ], string="Transaction Type")
    amount = fields.Float(string="Amount")
    currency_id = fields.Many2one('res.currency', string="Currency")

