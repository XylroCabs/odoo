from odoo import models, fields, api

class BankLedger(models.TransientModel):
    _name = 'bank.ledger.wizard'
    _description = 'Bank Ledger Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    journal_id = fields.Many2one('account.journal', string="Bank Journal", required=True,
                                 domain=[('type','=','bank')])

    def get_cash_book_lines(self):
        """Pull cash book transactions from account.move.line for the selected bank journal"""
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('move_id.state', '=', 'posted'),
            ('account_id', '=', self.journal_id.default_debit_account_id.id),
        ]
        return self.env['account.move.line'].search(domain, order='date asc')

    def action_view_cash_book(self):
        """Open a tree view of cash book transactions"""
        lines = self.get_cash_book_lines()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Cash Book Transactions',
            'res_model': 'account.move.line',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', lines.ids)],
        }
