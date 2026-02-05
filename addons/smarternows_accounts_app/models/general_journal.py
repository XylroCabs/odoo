from odoo import models, fields, api
from odoo.exceptions import ValidationError

class GeneralJournal(models.Model):
    _name = 'general.journal'
    _description = 'General Journal'

    name = fields.Char(string="Reference", required=True)
    date = fields.Date(string="Date", required=True)
    journal_id = fields.Many2one('account.journal', string="Journal", required=True)
    line_ids = fields.One2many('general.journal.line', 'journal_id', string="Journal Lines")
    move_id = fields.Many2one('account.move', string="Posted Move", readonly=True)

    @api.constrains('line_ids')
    def _check_balance(self):
        for journal in self:
            total_debit = sum(line.debit for line in journal.line_ids)
            total_credit = sum(line.credit for line in journal.line_ids)
            if round(total_debit, 2) != round(total_credit, 2):
                raise ValidationError(
                    "Journal is not balanced: Debits (%.2f) ≠ Credits (%.2f)" % (total_debit, total_credit)
                )

    def action_post(self):
        """Create and post an account.move from this general journal"""
        for journal in self:
            # Constraint already ensures balance
            move_vals = {
                'ref': journal.name,
                'date': journal.date,
                'journal_id': journal.journal_id.id,
                'line_ids': [],
            }
            lines = []
            for line in journal.line_ids:
                lines.append((0, 0, {
                    'account_id': line.account_id.id,
                    'partner_id': line.partner_id.id if line.partner_id else False,
                    'name': line.description or journal.name,
                    'debit': line.debit,
                    'credit': line.credit,
                }))
            move_vals['line_ids'] = lines
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            journal.move_id = move.id


class GeneralJournalLine(models.Model):
    _name = 'general.journal.line'
    _description = 'General Journal Line'

    journal_id = fields.Many2one('general.journal', string="Journal")
    account_id = fields.Many2one('account.account', string="Account", required=True)
    debit = fields.Float(string="Debit")
    credit = fields.Float(string="Credit")
    partner_id = fields.Many2one('res.partner', string="Partner")
    description = fields.Char(string="Description")
