# def button_register_payment_new(self):
import logging

logger = logging.getLogger(__name__)


def _process_csv_new(self, parsed_csv, country):
    state_model = self.env["res.country.state"]
    zip_model = self.env["res.city.zip"]
    res_city_model = self.env["res.city"]
    # Store current record list
    old_zips = set(zip_model.search([("city_id.country_id", "=", country.id)]).ids)
    search_zips = len(old_zips) > 0
    old_cities = set(res_city_model.search([("country_id", "=", country.id)]).ids)
    search_cities = len(old_cities) > 0
    current_states = state_model.search([("country_id", "=", country.id)])
    search_states = len(current_states) > 0
    max_import = self.env.context.get("max_import", 0)
    logger.info("Starting to create the cities and/or city zip entries")
    # Pre-create states and cities
    state_dict = self._create_states(parsed_csv, search_states, max_import, country)
    city_dict = self._create_cities(
        parsed_csv, search_cities, max_import, state_dict, country
    )
    # Zips
    zip_vals_list = []
    for i, row in enumerate(parsed_csv):
        if max_import and i == max_import:
            break
        # Don't search if there aren't any records
        zip_code = False
        state = state_dict[row[country.geonames_state_code_column or 4]]
        if search_zips:
            zip_code = self._select_zip(row, country, state)
        if not zip_code:
            city_id = city_dict[(self.transform_city_name(row[2], country), state.id)]
            zip_vals = self.prepare_zip(row, city_id)
            if zip_vals not in zip_vals_list:
                zip_vals_list.append(zip_vals)
        else:
            old_zips -= set(zip_code.ids)
    # TODO: update prepare zip vals group
    if country.code == "TH":
        # We don't want to create zip codes for other countries
        zip_vals_list = self.update_prepare_zip_vals(zip_vals_list)
    zip_model.create(zip_vals_list)
    if not max_import:
        if old_zips:
            self._action_remove_old_records("res.city.zip", old_zips, country)
        old_cities -= set(city_dict.values())
        if old_cities:
            self._action_remove_old_records("res.city", old_cities, country)
    logger.info(
        "The wizard to create cities and/or city zip entries from "
        "geonames has been successfully completed."
    )
    return True
