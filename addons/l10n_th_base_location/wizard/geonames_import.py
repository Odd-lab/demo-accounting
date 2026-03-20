import csv
import logging
import os
from collections import defaultdict

from odoo import api, models

logger = logging.getLogger(__name__)


class CityZipGeonamesImport(models.TransientModel):
    _inherit = "city.zip.geonames.import"

    @api.model
    def get_and_parse_csv(self, country):
        if country.code == "TH":
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(path[:-6], "data/TH_th.csv")
            data_file = open(file_path, encoding="utf-8")
            data_file.seek(0)
            reader = csv.reader(data_file, delimiter="	")
            parsed_csv = [row for _, row in enumerate(reader)]
            data_file.close()
            return parsed_csv
        return super().get_and_parse_csv(country)

    @api.model
    def transform_city_name(self, city, country):
        city = super().transform_city_name(city, country)
        if country.code == "TH":
            parts = [p.strip() for p in city.split(",")]
            return parts[-1] if len(parts) > 1 else city
        else:
            return city

    def _create_cities(
        self, parsed_csv, search_cities, max_import, state_dict, country
    ):
        if country.code == "TH":
            city_name_map = {}
            city_vals_set = set()
            city_dict = {}
            for i, row in enumerate(parsed_csv):
                if max_import and i == max_import:
                    break
                state_code = row[country.geonames_state_code_column or 4]
                state = state_dict.get(state_code)
                if not state:
                    continue

                full_city_name = row[2].strip()
                parts = [p.strip() for p in full_city_name.split(",")]
                subdistrict_name = parts[0] if len(parts) > 1 else full_city_name
                district_name = parts[-1]
                city_key = (district_name, state.id)
                city_code = row[5].strip()
                if city_key not in city_name_map:
                    city_vals_set.add((district_name, state.id, country.id, city_code))
                    city_name_map[city_key] = []
                city_name_map[city_key].append(subdistrict_name)

            city_vals_list = [
                {
                    "name": name,
                    "state_id": state_id,
                    "country_id": country_id,
                    "code": code,
                }
                for name, state_id, country_id, code in city_vals_set
            ]
            logger.info("Importing %d cities", len(city_vals_list))
            created_cities = self.env["res.city"].create(city_vals_list)

            for i, vals in enumerate(city_vals_list):
                key = (vals["name"], vals["state_id"])
                city_dict[key] = created_cities[i].id
            subdistrict_vals = []
            for i, row in enumerate(parsed_csv):
                if max_import and i == max_import:
                    break

                full_city_name = row[2].strip()
                parts = [p.strip() for p in full_city_name.split(",")]
                subdistrict_name = parts[0] if len(parts) > 1 else full_city_name
                district_name = parts[-1]
                state_code = row[country.geonames_state_code_column or 4]
                state = state_dict.get(state_code)
                if not state:
                    continue

                city_key = (district_name, state.id)
                city_id = city_dict.get(city_key)
                if not city_id:
                    continue

                subdistrict_vals.append(
                    {
                        "name": subdistrict_name,
                        "local_name": subdistrict_name,
                        "code": row[6].strip(),
                        "city_id": city_id,
                        "country_id": country.id,
                    }
                )

            logger.info("Importing %d subdistricts", len(subdistrict_vals))
            self.env["res.country.subdistrict"].create(subdistrict_vals)

            return city_dict
        else:
            return super()._create_cities(
                parsed_csv, search_cities, max_import, state_dict, country
            )

    def update_prepare_zip_vals(self, zip_vals_list):
        grouped = defaultdict(list)
        for zip_val in zip_vals_list:
            grouped[zip_val["name"]].append(zip_val["city_id"])
        final_zip_vals = []
        for name, city_ids in grouped.items():
            cities = self.env["res.city"].browse(city_ids)
            combined_city_ids = list(set(cities.ids))
            combined_subdistrict_ids = list(
                {sub.id for city in cities for sub in city.subdistrict_ids}
            )
            final_zip_vals.append(
                {
                    "name": name,
                    "city_id": cities[0].id,
                    "city_ids": [(6, 0, combined_city_ids)],
                    "subdistrict_ids": [(6, 0, combined_subdistrict_ids)],
                }
            )

        return final_zip_vals
