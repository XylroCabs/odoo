from odoo import models, fields

class SaccoLoan(models.Model):
    _name = 'sacco.loan'
    _description = 'SACCO Loan'

    member_id = fields.Many2one('res.partner', required=True, domain=[('customer_rank','>',0)])
    loan_product_id = fields.Many2one('sacco.loan.product', required=True)
    amount = fields.Float(required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid')
    ], default='draft')
    journal_entry_id = fields.Many2one('account.move', string="Journal Entry")

    def action_disburse(self):
        for loan in self:
            product = loan.loan_product_id
            move_vals = {
                'ref': f'Loan Disbursement {loan.member_id.name}',
                'date': fields.Date.today(),
                'journal_id': product.journal_id.id,
                'line_ids': [
                    (0, 0, {
                        'name': 'Loan Receivable',
                        'account_id': product.receivable_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': loan.amount,
                        'credit': 0.0,
                    }),
                    (0, 0, {
                        'name': 'Bank',
                        'account_id': product.journal_id.default_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': 0.0,
                        'credit': loan.amount,
                    }),
                ]
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            loan.write({'state': 'disbursed', 'journal_entry_id': move.id})

