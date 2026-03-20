from datetime import timedelta

from odoo import _, api, models
from odoo.exceptions import UserError, ValidationError


class IrSequenceDateRange(models.Model):
    _inherit = "ir.sequence.date_range"

    @api.constrains("date_from", "date_to", "sequence_id")
    def _check_sequence_period_range(self):
        for sequence_id in self.mapped("sequence_id"):
            current_set = set()
            for rec in sequence_id.date_range_ids:
                if rec.date_from > rec.date_to:
                    raise UserError(
                        _("Invalid duration from %(rec.date_from)s to %(rec.date_to)s")
                    )

                range_days = rec.date_to - rec.date_from

                record_set = {
                    rec.date_from + timedelta(days=i)
                    for i in range(range_days.days + 1)
                }
                overlap_set = current_set.intersection(record_set)
                if overlap_set:
                    # pylint: disable=W8120
                    overlap_msg = _("{0}: {1}\nDate Overlap in period {2} - {3}.\n{4}")
                    raise ValidationError(
                        overlap_msg.format(
                            sequence_id.name,
                            sequence_id.code,
                            rec.date_from.strftime("%d/%m/%Y"),
                            rec.date_to.strftime("%d/%m/%Y"),
                            ", ".join(
                                map(lambda x: x.strftime("%d/%m/%Y"), overlap_set)
                            ),
                        )
                    )

                current_set = current_set.union(record_set)
