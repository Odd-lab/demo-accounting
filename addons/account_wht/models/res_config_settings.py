from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    wht_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Withholding Tax Sequence",
        related="company_id.wht_sequence_id",
        readonly=False,
    )
    pnd3_txt_format = fields.Text(
        related="company_id.pnd3_txt_format",
        readonly=False,
    )
    pnd53_txt_format = fields.Text(
        related="company_id.pnd53_txt_format",
        readonly=False,
    )
