from odoo import api, fields, models
from odoo.osv import expression


class CountryState(models.Model):
    _inherit = "res.country.state"
    _rec_names_search = ["name", "code", "local_name"]

    name = fields.Char(
        string="State Name",
        required=True,
    )
    local_name = fields.Char()
    code = fields.Char(
        required=True,
    )
    district_ids = fields.One2many(
        comodel_name="res.city",
        inverse_name="state_id",
        string="Districts",
    )
    country_id = fields.Many2one(
        comodel_name="res.country",
        default=lambda self: self.env.user.company_id.country_id,
    )

    @api.model
    def _search_display_name(self, name, args=None, operator="ilike", limit=100):
        domain = args or []
        if operator not in expression.NEGATIVE_TERM_OPERATORS and name:
            domain = [
                "|",
                "|",
                ("name", operator, name),
                ("local_name", operator, name),
                ("code", operator, name),
            ]
        return self._search(expression.AND([domain]), limit=limit)

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
