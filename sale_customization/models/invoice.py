from odoo import fields, models ,api

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'
    internal_remarks = fields.Text(string='Internal Remarks')