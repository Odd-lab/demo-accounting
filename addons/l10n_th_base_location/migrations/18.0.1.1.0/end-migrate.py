from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    country = env["res.country"].search([("code", "=", "TH")], limit=1)
    address_format = """%(house_number)s %(village_number)s %(village)s
%(building)s %(floor)s %(room_number)s
%(alley)s %(sub_alley)s
%(street)s
%(subdistrict_id)s %(city)s
%(zip)s
%(state_name)s"""
    if country:
        country.address_format = address_format

    env["res.partner.title"].search(
        [
            (
                "id",
                "in",
                [
                    env.ref("base.res_partner_title_madam").id,
                    env.ref("base.res_partner_title_miss").id,
                    env.ref("base.res_partner_title_mister").id,
                    env.ref("base.res_partner_title_doctor").id,
                    env.ref("base.res_partner_title_prof").id,
                ],
            )
        ]
    ).unlink()
