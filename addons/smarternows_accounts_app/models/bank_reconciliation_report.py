from odoo import models, fields

class BankReconciliationReportWizard(models.TransientModel):
    _name = 'bank.reconciliation.report.wizard'
    _description = 'Bank Reconciliation Report Wizard'

    statement_id = fields.Many2one('account.bank.statement', string="Bank Statement", required=True)

    def get_report_data(self):
        reconciled = []
        unreconciled = []
        for line in self.statement_id.line_ids:
            if line.move_id:
                reconciled.append({
                    'date': line.date,
                    'name': line.name,
                    'partner': line.partner_id.name if line.partner_id else '',
                    'amount': line.amount,
                    'move': line.move_id.name,
                })
            else:
                unreconciled.append({
                    'date': line.date,
                    'name': line.name,
                    'partner': line.partner_id.name if line.partner_id else '',
                    'amount': line.amount,
                })

        # Summary section
        opening_balance = self.statement_id.balance_start
        closing_balance = self.statement_id.balance_end_real
        reconciled_total = sum(line['amount'] for line in reconciled)
        unreconciled_total = sum(line['amount'] for line in unreconciled)
        difference = closing_balance - (opening_balance + reconciled_total + unreconciled_total)

        return {
            'statement': self.statement_id.name,
            'date': self.statement_id.date,
            'opening_balance': opening_balance,
            'closing_balance': closing_balance,
            'reconciled_total': reconciled_total,
            'unreconciled_total': unreconciled_total,
            'difference': difference,
            'reconciled': reconciled,
            'unreconciled': unreconciled,
        }

    def action_print_report(self):
        data = self.get_report_data()
        return self.env.ref('smarternows_accounts_app.action_report_bank_reconciliation').report_action(None, data=data)
