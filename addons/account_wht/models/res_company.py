from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    @api.model
    def _get_default_pnd3_txt_format(self):
        return (
            "%(partner_vat)s||"
            "%(title)s||"
            "%(firstname)s||"
            "%(lastname)s|||||"
            "%(house_number)s||%(alley)s|"
            "%(sub_alley)s|%(subdistrict)s|"
            "%(city)s|%(state)s|"
            "%(zip)s|%(document_date)s|"
            "%(type_income)s|%(tax_rate)s|"
            "%(base_amount)s|%(tax_amount)s|"
            "%(wht_payment)s||||||||||||"
        )

    @api.model
    def _get_default_pnd53_txt_format(self):
        return (
            "%(partner_vat)s||"
            "%(title)s||"
            "%(firstname)s||"
            "%(lastname)s|||||"
            "%(house_number)s||%(alley)s|"
            "%(sub_alley)s|%(subdistrict)s|"
            "%(city)s|%(state)s|"
            "%(zip)s|%(document_date)s|"
            "%(type_income)s|%(tax_rate)s|"
            "%(base_amount)s|%(tax_amount)s|"
            "%(wht_payment)s||||||||||||"
        )

    wht_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Withholding Tax Sequence",
    )
    pnd3_txt_format = fields.Text(
        default=_get_default_pnd3_txt_format,
    )
    pnd53_txt_format = fields.Text(
        default=_get_default_pnd53_txt_format,
    )

    # @api.constrains("pnd3_txt_format", "pnd53_txt_format")
    # def _check_pnd_txt_format(self):
    #     for company in self:
    #         address_fields = self.env["res.partner"]._formatting_address_fields()
    #         for field_name in ("pnd3_txt_format", "pnd53_txt_format"):
    #             txt_format = company[field_name]
    #             if not txt_format:
    #                 continue
    #             try:
    #                 txt_format % {key: "1" for key in address_fields}
    #             except (ValueError, KeyError) as err:
    #                 raise ValidationError(
    #                     self.env._("%s contains an invalid format key.")
    #                     % company._fields[field_name].string
    #                 ) from err

    def _create_wht_per_company_sequences(self):
        vals_list = []

        for company in self:
            vals_list.append(
                {
                    "name": f"{company.name} - Withholding Tax Sequence",
                    "code": "wht.sequence",
                    "company_id": company.id,
                    "prefix": "WHT/%(range_y)s%(range_month)s",
                    "padding": 4,
                    "implementation": "standard",
                    "number_next": 1,
                    "number_increment": 1,
                    "use_date_range": True,
                }
            )
        if vals_list:
            sequences = self.env["ir.sequence"].create(vals_list)
            for rec in sequences:
                rec.company_id.wht_sequence_id = rec.id

    def th_split_tax_number(self, option="1"):
        return self.partner_id.th_split_tax_number(option)
