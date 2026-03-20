from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_address_details = fields.Boolean(
        related="country_id.is_address_details",
    )
    prefix = fields.Char()
    suffix = fields.Char()
    house_number = fields.Char()
    village_number = fields.Char()
    village = fields.Char()
    building = fields.Char()
    floor = fields.Char()
    room_number = fields.Char()
    alley = fields.Char()
    sub_alley = fields.Char()
    subdistrict = fields.Char()
    subdistrict_id = fields.Many2one(
        comodel_name="res.country.subdistrict",
        domain="[('city_id', '=?', city_id), ('state_id', '=?', state_id)]",
        store=True,
        readonly=False,
        index=True,
    )
    city_id = fields.Many2one(
        comodel_name="res.city",
        string="District",
        domain="""[
            ('state_id', '=?', state_id),
            ('country_id', '=', country_id),
        ] + (
            subdistrict_id and [('subdistrict_ids', 'in', [subdistrict_id])] or []
        )""",
    )
    city = fields.Char(
        compute="_compute_city",
        store=True,
    )
    country_id = fields.Many2one(
        default=lambda self: self.env.user.company_id.country_id,
    )
    zip = fields.Char(
        related="zip_id.name",
    )
    zip_id = fields.Many2one(
        domain="[('country_id', '=', country_id), ('city_id', '=?', city_id)]",
    )
    complete_name = fields.Char(
        compute="_compute_complete_name",
        size=256,
        store=True,
    )
    child_ids = fields.One2many(
        domain=[],
    )
    branch_type = fields.Selection(
        selection=[
            ("hq", "Head Office"),
            ("branch", "Branch"),
        ],
        string="Company Type",
        required=True,
        default="hq",
    )
    branch_number = fields.Char()

    @api.constrains("vat", "parent_id", "country_id")
    def _check_vat_unique(self):
        for rec in self:
            if rec.vat:
                if rec.country_id.is_enforce_vat and rec.same_vat_partner_id:
                    raise ValidationError(
                        self.env._("ID Card/Tax ID %s Contact is already exists!")
                        % (rec.vat)
                    )

    @api.depends("name", "company_type", "lang", "title")
    def _compute_complete_name(self):
        for rec in self:
            lang = rec._context.get("lang", "en_EN")
            rec.complete_name = rec._complete_name(prefer_lang=lang)

    @api.depends("vat", "company_id", "company_registry")
    def _compute_same_vat_partner_id(self):
        res = super()._compute_same_vat_partner_id()
        for partner in self:
            partner_id = partner._origin.id
            Partner = self.with_context(active_test=False).sudo()
            domain = [
                ("vat", "=", partner.vat),
                ("company_id", "in", [False, partner.company_id.id]),
            ]
            if partner_id:
                domain += [
                    ("id", "!=", partner_id),
                    "!",
                    ("id", "child_of", partner_id),
                ]
            partner.same_vat_partner_id = (
                bool(partner.vat)
                and not partner.parent_id
                and Partner.search(domain, limit=1)
            )
            # check company_registry
            domain = [
                ("company_registry", "=", partner.company_registry),
                ("company_id", "in", [False, partner.company_id.id]),
            ]
            if partner_id:
                domain += [
                    ("id", "!=", partner_id),
                    "!",
                    ("id", "child_of", partner_id),
                ]
            if partner.country_id.is_enforce_vat:
                domain += [
                    ("country_id", "=", partner.country_id.id),
                ]
            partner.same_company_registry_partner_id = (
                bool(partner.company_registry)
                and not partner.parent_id
                and Partner.search(domain, limit=1)
            )
        return res

    def _complete_name(self, prefer_lang="", show_branch=False):
        self.ensure_one()
        if not self.name:
            return ""
        if related_name := self.parent_id and self.parent_id._complete_name(
            prefer_lang
        ):
            return " - ".join([related_name, self.name])
        return self.name

    def action_open_form_view(self):
        return self._get_records_action(
            name="Contact",
        )

    def _get_format_address_wht(self):
        return (
            "%(house_number)s %(village_number)s %(village)s "
            "%(building)s %(room_number)s %(floor)s "
            "%(alley)s %(sub_alley)s %(street)s "
            "%(subdistrict_id)s %(city)s %(zip)s %(state_name)s"
        )

    def _get_address_partner(self):
        self.ensure_one()
        _, args = self._prepare_display_address(without_company=False)
        return self._get_format_address_wht() % args

    @api.model
    def _address_fields(self):
        res = super()._address_fields()
        res.extend(
            [
                "house_number",
                "village_number",
                "village",
                "building",
                "room_number",
                "floor",
                "alley",
                "sub_alley",
                "subdistrict_id",
            ]
        )
        return res

    def _prepare_display_address(self, without_company=False):
        address, args = super()._prepare_display_address(without_company)
        return address, {
            **args,
            "subdistrict_id": self.subdistrict_id.name or "",
        }

    def _get_branch_number(self):
        if self.branch_type == "hq":
            return "0000"
        return self.branch_number or "0000"
