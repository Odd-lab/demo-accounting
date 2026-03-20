from odoo import fields, models


class ResCountrySubdistrict(models.Model):
    _name = "res.country.subdistrict"
    _description = "Subdistrict"
    _rec_names_search = ["name", "code", "local_name"]

    name = fields.Char(
        string="Subdistrict",
    )
    local_name = fields.Char()
    code = fields.Char(
        required=True,
    )
    city_id = fields.Many2one(
        comodel_name="res.city",
        string="District",
    )
    city_code = fields.Char(
        related="city_id.code",
        store=True,
    )
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        related="city_id.state_id",
        store=True,
    )
    state_code = fields.Char(
        related="city_id.state_id.code",
        store=True,
    )
    zip_ids = fields.Many2many(
        comodel_name="res.city.zip",
        string="Zips in Subdistrict",
        relation="res_city_zip_res_country_subdistrict_rel",
        column1="res_country_subdistrict_id",
        column2="res_city_zip_id",
    )
    country_id = fields.Many2one(
        comodel_name="res.country",
    )

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
