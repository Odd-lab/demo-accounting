from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _post_logout(cls):
        request.future_response.set_cookie("color_scheme", max_age=0)

    def webclient_rendering_context(self):
        return {
            "session_info": self.session_info(),
        }

    def session_info(self):
        # ICP = self.env['ir.config_parameter'].sudo()

        # if self.env.user.has_group('base.group_system'):
        #     warn_enterprise = 'admin'
        # elif self.env.user._is_internal():
        #     warn_enterprise = 'user'
        # else:
        #     warn_enterprise = False

        result = super().session_info()
        # result['support_url'] = "https://www.odoo.com/help"
        # if warn_enterprise:
        #     result['warning'] = warn_enterprise
        #     result['expiration_date'] = ICP.get_param('database.expiration_date')
        #     result['expiration_reason'] = ICP.get_param('database.expiration_reason')
        return result
