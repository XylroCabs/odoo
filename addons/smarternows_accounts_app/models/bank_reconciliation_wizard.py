from odoo import models, fields, api
from odoo.exceptions import UserError

class BankReconciliationWizard(models.TransientModel):
    _name = 'bank.reconciliation.wizard'
    _description = 'Bank Reconciliation Wizard'

    statement_id = fields.Many2one('account.bank.statement', string="Bank Statement", required=True)
    journal_id = fields.Many2one('account.journal', string="Bank Journal", required=True,
                                 domain=[('type','=','bank')])
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")

    def get_statement_lines(self):
        return self.statement_id.line_ids

    def get_cash_book_lines(self):
        domain = [
            ('date', '>=', self.date_from) if self.date_from else ('id','!=',False),
            ('date', '<=', self.date_to) if self.date_to else ('id','!=',False),
            ('move_id.state', '=', 'posted'),
            ('account_id', '=', self.journal_id.default_debit_account_id.id),
        ]
        return self.env['account.move.line'].search(domain, order='date asc')

    def action_reconcile(self):
        """Match statement lines with cash book entries by amount and partner"""
        statement_lines = self.get_statement_lines()
        cash_book_lines = self.get_cash_book_lines()
        reconciled = []
        for st_line in statement_lines:
            match = cash_book_lines.filtered(
                lambda l: abs(l.balance - st_line.amount) < 0.01 and l.partner_id == st_line.partner_id
            )
            if match:
                st_line.write({'move_id': match[0].move_id.id})
                reconciled.append((st_line.name, match[0].move_id.name))
        if not reconciled:
            raise UserError("No matches found for reconciliation.")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reconciled Entries',
            'res_model': 'account.bank.statement.line',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', statement_lines.ids)],
        }
