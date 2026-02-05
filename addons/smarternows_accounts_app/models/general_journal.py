from odoo import models, fields

class GeneralJournal(models.Model):
    _name = 'general.journal'
    _description = 'General Journal'

    name = fields.Char(string="Reference", required=True)
    date = fields.Date(string="Date", required=True)
    journal_id = fields.Many2one('account.journal', string="Journal", required=True)
    line_ids = fields.One2many('general.journal.line', 'journal_id', string="Journal Lines")

class GeneralJournalLine(models.Model):
    _name = 'general.journal.line'
    _description = 'General Journal Line'

    journal_id = fields.Many2one('general.journal', string="Journal")
    account_id = fields.Many2one('account.account', string="Account", required=True)
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    partner_id = fields.Many2one('res.partner', string="Partner")
    description = fields.Char(string="Description")
