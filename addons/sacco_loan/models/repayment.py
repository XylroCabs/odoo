from odoo import models, fields

class SaccoRepayment(models.Model):
    _name = 'sacco.repayment'
    _description = 'Loan Repayment'

    loan_id = fields.Many2one('sacco.loan', required=True)
    schedule_id = fields.Many2one('sacco.repayment.schedule')
    date = fields.Date(default=fields.Date.today)
    principal_amount = fields.Float(required=True)
    interest_amount = fields.Float(default=0.0)
    journal_entry_id = fields.Many2one('account.move', string="Journal Entry")

    def action_post_repayment(self):
        for repayment in self:
            loan = repayment.loan_id
            product = loan.loan_product_id
            total_amount = repayment.principal_amount + repayment.interest_amount

            move_vals = {
                'ref': f'Loan Repayment {loan.member_id.name}',
                'date': repayment.date,
                'journal_id': product.journal_id.id,
                'line_ids': [
                    # Debit Bank
                    (0, 0, {
                        'name': 'Bank',
                        'account_id': product.journal_id.default_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': total_amount,
                        'credit': 0.0,
                    }),
                    # Credit Loan Receivable
                    (0, 0, {
                        'name': 'Loan Principal',
                        'account_id': product.receivable_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': 0.0,
                        'credit': repayment.principal_amount,
                    }),
                    # Credit Interest Income
                    (0, 0, {
                        'name': 'Loan Interest',
                        'account_id': product.interest_income_account_id.id,
                        'partner_id': loan.member_id.id,
                        'debit': 0.0,
                        'credit': repayment.interest_amount,
                    }),
                ]
            }
            move = self.env['account.move'].create(move_vals)
            move.action_post()
            repayment.write({'journal_entry_id': move.id})
            if repayment.schedule_id:
                repayment.schedule_id.paid = True
