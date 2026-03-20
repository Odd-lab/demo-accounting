from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    taxes = env["account.tax"].search([("is_withholding_tax_on_payment", "=", True)])
    for tax in taxes:
        tax._onchange_is_withholding_tax_on_payment()
