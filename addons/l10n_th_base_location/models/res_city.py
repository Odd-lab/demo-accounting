from odoo import api, fields, models


class City(models.Model):
    _inherit = "res.city"
    _rec_names_search = ["name", "code", "local_name"]

    name = fields.Char(
        string="District",
        required=True,
    )
    local_name = fields.Char()
    code = fields.Char()
    state_code = fields.Char(
        related="state_id.code",
        store=True,
    )
    subdistrict_ids = fields.One2many(
        comodel_name="res.country.subdistrict",
        inverse_name="city_id",
    )
    country_id = fields.Many2one(
        comodel_name="res.country",
        default=lambda self: self.env.user.company_id.country_id,
    )
    zip_ids = fields.Many2many(
        comodel_name="res.city.zip",
        string="Zips in City",
        relation="res_city_res_city_zip_rel",
        column1="res_city_id",
        column2="res_city_zip_id",
    )

    @api.onchange("country_id")
    def _onchange_country_id(self):
        for rec in self:
            if rec.state_id.country_id != rec.country_id:
                rec.state_id = False

    def _compute_display_name(self):
        for rec in self:
            lang = rec._context.get("lang", "en_EN")
            rec.display_name = rec._complete_name(prefer_lang=lang)

    def _complete_name(self, prefer_lang=""):
        self.ensure_one()
        if not self.name:
            return ""
        self.local_name = self.with_context(lang=prefer_lang).name
        return self.local_name
