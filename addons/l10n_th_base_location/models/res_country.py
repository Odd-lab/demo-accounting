from odoo import fields, models


class Country(models.Model):
    _inherit = "res.country"

    is_address_details = fields.Boolean(
        string="Address Details (TH)",
        help="Check this box to show address detail ex. Building, Alley etc.",
    )
    is_state_city_easy_fill = fields.Boolean(
        string="State-City Easy Fill",
    )
    is_enforce_vat = fields.Boolean()
