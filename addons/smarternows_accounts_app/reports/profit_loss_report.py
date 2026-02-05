from odoo import models

class ProfitLossReport(models.AbstractModel):
    _name = 'report.smarternows_accounts_app.profit_loss_report'
    _description = 'Profit & Loss Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].search([('state', '=', 'posted')])
        income = sum(docs.filtered(lambda m: m.move_type == 'out_invoice').mapped('amount_total'))
        expenses = sum(docs.filtered(lambda m: m.move_type == 'in_invoice').mapped('amount_total'))
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'income': income,
            'expenses': expenses,
            'profit_loss': income - expenses,
        }
