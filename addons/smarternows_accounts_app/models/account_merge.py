from odoo import models, fields

class AccountMerge(models.Model):
    _name = 'account.merge'
    _description = 'Unified Accounting View'

    name = fields.Char(string="Transaction Name")
    transaction_type = fields.Selection([
        ('sale', 'Sale'),
        ('purchase', 'Purchase'),
        ('bank', 'Bank'),
        ('journal', 'Journal'),
        ('asset', 'Asset'),
    ], string="Type")
    amount = fields.Float(string="Amount")
    date = fields.Date(string="Date")
