from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = 'res.partner'

    def _prepare_display_address(self, without_company=False):
        res = super()._prepare_display_address()
        #
        # print(res[1])
        # print("========================")
        # exit()
        return  res