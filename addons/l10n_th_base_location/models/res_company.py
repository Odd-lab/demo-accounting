from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    house_number = fields.Char(
        compute="_compute_address",
        inverse="_inverse_house_number",
    )
    village_number = fields.Char(
        compute="_compute_address",
        inverse="_inverse_village_number",
    )
    village = fields.Char(
        compute="_compute_address",
        inverse="_inverse_village",
    )
    building = fields.Char(
        compute="_compute_address",
        inverse="_inverse_building",
    )
    floor = fields.Char(
        compute="_compute_address",
        inverse="_inverse_floor",
    )
    room_number = fields.Char(
        compute="_compute_address",
        inverse="_inverse_room_number",
    )
    alley = fields.Char(
        compute="_compute_address",
        inverse="_inverse_alley",
    )
    sub_alley = fields.Char(
        compute="_compute_address",
        inverse="_inverse_sub_alley",
    )
    subdistrict_id = fields.Many2one(
        comodel_name="res.country.subdistrict",
        domain="[('city_id', '=?', city_id)]",
        compute="_compute_address",
        inverse="_inverse_subdistrict_id",
    )
    city_id = fields.Many2one(
        comodel_name="res.city",
        string="District",
        domain="[('state_id', '=?', state_id)]",
    )
    is_address_details = fields.Boolean()
    is_show_company_registry = fields.Boolean(
        compute="_compute_is_show_company_registry",
    )

    @api.constrains("vat", "country_id")
    def _check_vat_is_correct(self):
        for rec in self:
            if rec.vat:
                vat = [num for num in rec.vat if num.isalnum() or num.isspace()]
                vat = "".join(vat)
                th_country_id = self.env.ref("base.th")
                if rec.country_id == th_country_id:
                    if len(vat) != 13:
                        raise ValidationError(_("ID Card/Tax ID Must Use 13 Digits"))
                    if not vat.isnumeric():
                        raise ValidationError(
                            _("ID Card/Tax ID is not correct, Please check.")
                        )

    @api.constrains("zip_id", "country_id", "city_id", "state_id")
    def _check_zip(self):
        if self.env.context.get("skip_check_zip"):
            return
        for rec in self:
            if not rec.zip_id or not rec.zip_id.city_id:
                continue
            if rec.zip_id.city_id.state_id != rec.state_id:
                raise ValidationError(
                    _(
                        "The state of the partner %(name)s differs from that in "
                        "location %(zip)s",
                        name=rec.name,
                        zip=rec.zip_id.name,
                    )
                )
            if rec.zip_id.city_id.country_id != rec.country_id:
                raise ValidationError(
                    _(
                        "The country of the partner %(name)s differs from that in "
                        "location %(zip)s",
                        name=rec.name,
                        zip=rec.zip_id.name,
                    )
                )
            if rec.zip_id.city_id != rec.city_id:
                raise ValidationError(
                    _(
                        "The city of partner %(name)s differs from that in "
                        "location %(zip)s",
                        name=rec.name,
                        zip=rec.zip_id.name,
                    )
                )

    def _compute_is_show_company_registry(self):
        for rec in self:
            rec.is_show_company_registry = (
                False if rec.country_id == self.env.ref("base.th") else True
            )

    def _inverse_house_number(self):
        for company in self:
            company.partner_id.house_number = company.house_number

    def _inverse_village_number(self):
        for company in self:
            company.partner_id.village_number = company.village_number

    def _inverse_village(self):
        for company in self:
            company.partner_id.village = company.village

    def _inverse_building(self):
        for company in self:
            company.partner_id.building = company.building

    def _inverse_floor(self):
        for company in self:
            company.partner_id.floor = company.floor

    def _inverse_room_number(self):
        for company in self:
            company.partner_id.room_number = company.room_number

    def _inverse_alley(self):
        for company in self:
            company.partner_id.alley = company.alley

    def _inverse_sub_alley(self):
        for company in self:
            company.partner_id.sub_alley = company.sub_alley

    def _inverse_subdistrict_id(self):
        for company in self.with_context(skip_check_zip=True):
            company.partner_id.subdistrict_id = company.subdistrict_id

    @api.onchange("country_id")
    def _onchange_country_id(self):
        res = super()._onchange_country_id()
        self.is_address_details = self.country_id.is_address_details
        return res

    def _get_company_address_field_names(self):
        res = super()._get_company_address_field_names()
        res += [
            "house_number",
            "village_number",
            "village",
            "building",
            "floor",
            "room_number",
            "alley",
            "sub_alley",
            "subdistrict_id",
        ]
        return res
