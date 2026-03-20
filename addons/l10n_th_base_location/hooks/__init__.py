from .geonames_import import _process_csv_new


from odoo.addons.base_location_geonames_import.wizard.geonames_import import (
    CityZipGeonamesImport,
)


def post_load_hook():
    CityZipGeonamesImport._process_csv = _process_csv_new
