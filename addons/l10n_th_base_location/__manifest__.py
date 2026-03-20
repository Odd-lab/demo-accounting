{
    "name": "Base Location Thailand",
    "summary": """
        Import Thailand zip entries from Geonames
    """,
    "author": "Odd lab",
    "countries": ["th"],
    "category": "Localizations",
    "website": "https://github.com/tao-thewarat",
    "version": "18.0.1.1.0",
    "license": "LGPL-3",
    "contributors": [
        "tao-thewarat",
    ],
    "depends": [
        "base_location_geonames_import",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/res.partner.title.csv",
        "views/res_city_views.xml",
        "views/res_city_zip_views.xml",
        "views/res_country_state_views.xml",
        "views/res_country_subdistrict_views.xml",
        "views/res_country_view.xml",
        "views/res_partner_view.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
    "application": False,
    "post_load": "post_load_hook",
}
