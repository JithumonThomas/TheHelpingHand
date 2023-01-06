from odoo import fields, models, api


class DeliveryOrderInherit(models.Model):
    _inherit = 'stock.picking'

    # @api.model
    #

    # def _remarks(self):
    #
    #     active_id = self.env.context.get('active_id')
    #
    #     sale_order_internal_remarks = self.env['sale.order'].sudo().search([('id', '=', active_id)])
    #
    #     if sale_order_internal_remarks:
    #         return  sale_order_internal_remarks.internal_remarks
    #         # return active_id
    internal_remarks = fields.Text(string='Internal Remarks')
    order_date = fields.Datetime(related='sale_id.date_order',string='Order Date')
    team_id = fields.Many2one('crm.team',related='sale_id.team_id', string='Sales Team')
    remarks = fields.Text(string='Remarks', readonly=True)

