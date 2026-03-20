{
    "name": "Withholding Tax On Payment",
    "summary": "Create and manage withholding tax documents linked to payments",
    "description": "Manage Withholding Tax (WHT) documents linked to Payments, including certificate report printing and XLSX export.",
    "version": "18.0.1.1.1",
    "category": "Accounting",
    "author": "Odd lab",
    "license": "LGPL-3",
    "company": "Odd lab",
    "website": "https://github.com/tao-thewarat",
    "depends": [
        "l10n_account_withholding_tax",
        "l10n_th_base_location",
        "date_range_sequence",
        "partner_firstname",
        "l10n_th_amount_to_text",
    ],
    "external_dependencies": {
        "python": [
            "openpyxl",
        ],
    },
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/paperformat.xml",
        "data/report_data.xml",
        "reports/wht_certificate_report.xml",
        "wizards/account_payment_register_views.xml",
        "views/account_withholding_tax_views.xml",
        "views/res_config_settings_views.xml",
        "views/account_payment_views.xml",
        "views/account_tax_views.xml",
        "views/menuitems.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "account_wht/static/src/css/*.css",
            "account_wht/static/src/css/*.scss",
        ],
    },
    "installable": True,
    "application": False,
}
