from odoo import models, fields

class SaccoRepayment(models.Model):
    _name = 'sacco.repayment'
    _description = 'Loan Repayment'

    loan_id = fields.Many2one('sacco.loan', required=True)
    date = fields.Date(default=fields.Date.today)
    amount = fields.Float(required=True)
    journal_entry_id = fields.Many2one('account.move', string="Journal Entry")

    def action_post_repayment(self):
        for repayment in self:
            loan = repayment.loan_id
            product = loan.loan_product_id
            move_vals = {
                'ref': f'Loan Repayment {loan.member_id.name}',
                'date': repayment.date,
                'journal_id': product.journal_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': 'Bank',
                        'account_id': product.journal_id.default_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': repayment.amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {
                        'name': 'Loan Receivable',
                        'account_id': product.receivable_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': 0.0,
                        'credit': repayment.amount,
                    }),
                ]
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            repayment.write({'journal_entry_id': move.id})
