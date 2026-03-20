from odoo import api, fields, models


class AccountWithholdingTaxLine(models.Model):
    _name = "account.withholding.tax.line"
    _inherit = "account.withholding.line"
    _description = "Account Withholding Tax Line"
    _check_company_auto = True

    withholding_tax_id = fields.Many2one(
        comodel_name="account.withholding.tax",
        required=True,
        ondelete="cascade",
    )

    @api.depends("withholding_tax_id.company_id")
    def _compute_company_id(self):
        for rec in self:
            rec.company_id = rec.withholding_tax_id.company_id

    @api.depends("withholding_tax_id.document_date")
    def _compute_comodel_date(self):
        for rec in self:
            rec.comodel_date = rec.withholding_tax_id.document_date

    @api.depends("withholding_tax_id.wht_payment")
    def _compute_comodel_payment_type(self):
        for rec in self:
            rec.comodel_payment_type = rec.withholding_tax_id.payment_id.payment_type

    @api.depends("withholding_tax_id.company_id.currency_id")
    def _compute_comodel_currency_id(self):
        for rec in self:
            rec.comodel_currency_id = rec.withholding_tax_id.company_id.currency_id

    @api.depends("withholding_tax_id.payment_id.payment_type")
    def _compute_type_tax_use(self):
        for rec in self:
            rec.type_tax_use = (
                "purchase"
                if rec.withholding_tax_id.payment_id.payment_type == "outbound"
                else "sale"
            )

    def _get_comodel_partner(self):
        self.ensure_one()
        return self.withholding_tax_id.partner_id or self.env["res.partner"]

    def _get_valid_liquidity_accounts(self):
        self.ensure_one()
        pay = self.withholding_tax_id.payment_id
        return pay._get_valid_liquidity_accounts() if pay else ()

    def _get_merge_domain_from_vals(self, vals):
        domain = [
            ("withholding_tax_id", "=", vals.get("withholding_tax_id")),
            ("tax_section", "=", vals.get("tax_section")),
        ]
        if vals.get("tax_section") == "6":
            domain.append(("other", "=", vals.get("other") or False))
        return domain

    def _prepare_merge_vals(self, line, vals):
        for field_name in ["base_amount", "amount"]:
            vals[field_name] = (line[field_name] or 0.0) + (vals.get(field_name) or 0.0)
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                vals.get("withholding_tax_id")
                and vals.get("tax_section")
                and (
                    wht_line := self.search(
                        self._get_merge_domain_from_vals(vals),
                        limit=1,
                    )
                )
            ):
                return wht_line.write(self._prepare_merge_vals(wht_line, vals))
        return super().create(vals_list)
