from odoo import models, fields
from datetime import timedelta

class SaccoLoan(models.Model):
    _name = 'sacco.loan'
    _description = 'SACCO Loan'

    member_id = fields.Many2one('res.partner', required=True, domain=[('customer_rank','>',0)])
    loan_product_id = fields.Many2one('sacco.loan.product', required=True)
    amount = fields.Float(required=True)
    term_months = fields.Integer(required=True)
    interest_rate = fields.Float(default=12.0)  # annual %
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
        ('repaid', 'Repaid')
    ], default='draft')
    journal_entry_id = fields.Many2one('account.move', string="Journal Entry")
    schedule_ids = fields.One2many('sacco.repayment.schedule', 'loan_id', string="Repayment Schedule")

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

            # generate repayment schedule after disbursement
            loan.generate_repayment_schedule()

    def generate_repayment_schedule(self):
        """Create monthly schedule with principal + interest split"""
        monthly_rate = self.interest_rate / 12 / 100
        principal_per_month = self.amount / self.term_months

        # clear old schedule if regenerating
        self.schedule_ids.unlink()

        for i in range(self.term_months):
            due_date = fields.Date.today() + timedelta(days=30*(i+1))
            interest = (self.amount - (principal_per_month * i)) * monthly_rate

            self.env['sacco.repayment.schedule'].create({
                'loan_id': self.id,
                'due_date': due_date,
                'principal_amount': principal_per_month,
                'interest_amount': interest,
            })
