from odoo import fields, models ,api

class SaleOrderTemplateInherit(models.Model):
    _inherit = 'sale.order.template'
    product_category_id = fields.Many2one('product.category',string='Product Category')
    team_id = fields.Many2one('crm.team', string='Sales Team')
