from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    type_income = fields.Char()

    @api.onchange("is_withholding_tax_on_payment")
    def _onchange_is_withholding_tax_on_payment(self):
        for rec in self:
            if rec.is_withholding_tax_on_payment and not rec.withholding_sequence_id:
                rec.withholding_sequence_id = rec.env.ref(
                    "account_wht.account_wht_sequence"
                )
