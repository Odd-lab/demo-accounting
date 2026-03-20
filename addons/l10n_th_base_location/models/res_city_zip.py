from odoo import fields, models


class ResCityZip(models.Model):
    _inherit = "res.city.zip"

    subdistrict_ids = fields.Many2many(
        comodel_name="res.country.subdistrict",
        relation="res_city_zip_res_country_subdistrict_rel",
        column1="res_city_zip_id",
        column2="res_country_subdistrict_id",
    )
    city_id = fields.Many2one(
        string="District",
    )
    city_ids = fields.Many2many(
        comodel_name="res.city",
        string="Districts",
        relation="res_city_res_city_zip_rel",
        column1="res_city_zip_id",
        column2="res_city_id",
    )
