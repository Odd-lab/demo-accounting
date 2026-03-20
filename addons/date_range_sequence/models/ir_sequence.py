import calendar
from datetime import timedelta

from odoo import api, fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    date_range = fields.Selection(
        selection=[
            ("day", "Day"),
            ("week", "Week"),
            ("month", "Month"),
            ("year", "Year"),
        ],
        string="Range",
    )

    @api.onchange("use_date_range")
    def _onchange_use_date_range(self):
        self.date_range = self.use_date_range and "year" or False

    # Overwrite standard odoo
    def _create_date_range_seq(self, date):
        date_from, date_to = self._get_period(
            current_date=fields.Date.from_string(date)
        )
        return (
            self.env["ir.sequence.date_range"]
            .sudo()
            .create(
                {
                    "date_from": date_from,
                    "date_to": date_to,
                    "sequence_id": self.id,
                }
            )
        )

    def _get_period(self, current_date):
        if self.date_range == "month":
            eom_day = calendar.monthrange(current_date.year, current_date.month)[1]
            date_from = current_date.replace(day=1)
            date_to = current_date.replace(day=eom_day)
        elif self.date_range == "week":
            date_from = current_date - timedelta(days=current_date.weekday())
            date_to = date_from + timedelta(days=6)
        elif self.date_range == "day":
            date_from = current_date
            date_to = current_date
        else:
            # Range in year or empty range
            date_from = current_date.replace(month=1, day=1)
            date_to = current_date.replace(month=12, day=31)
        return date_from, date_to
