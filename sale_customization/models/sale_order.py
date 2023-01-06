from odoo import fields, models, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        create_id = super(SaleOrderInherit, self).create(vals)
        for rec in create_id:
            users = []
            context = None
            for usr in rec.sale_order_template_team_id.member_ids:
                users.append(usr.partner_id.id)
            support_team = self.env['res.partner'].search(
                [('email', '=', 'business_support_team@thehelpinghand.org.sg')])
            if support_team:
                users.append(support_team.id)
            rec.message_subscribe(users, None)
            return create_id

    def write(self, vals):
        if self.invoice_ids:
            print("====================")
            if 'remarks' in  vals:
                for invoice in self.invoice_ids:
                    print(invoice)
                    invoice.write({'remarks':vals['remarks']})


        if self.picking_ids:

            if len(self.picking_ids) > 1:
                ids = []
                for picking_ids in self.picking_ids:
                        ids.append(picking_ids.id)
                sorted_list = sorted(ids)
                do_pick = self.env['stock.picking'].sudo().search([('id', '=', sorted_list[-1])])
                if 'preferred_delivery_date' in vals:
                    do_pick.write(
                        {'scheduled_date': vals['preferred_delivery_date'],
                         'date_deadline': vals['preferred_delivery_date']})
                    self.write({'scheduled_delivery_date': do_pick.scheduled_date})
            else:
                do_pick = self.picking_ids

                if 'preferred_delivery_date' in vals:
                    do_pick.write(
                        {'scheduled_date': vals['preferred_delivery_date'],
                         'date_deadline': vals['preferred_delivery_date']})
                    self.write({'scheduled_delivery_date': do_pick.scheduled_date})

        res = super(SaleOrderInherit, self)
        if vals:

            for rec in self:
                member_ids = []
                if rec.sale_order_template_team_id.member_ids:

                    for us_rec in rec.sale_order_template_team_id.member_ids:
                        member_ids.append(us_rec.partner_id.id)
                if 'team_id' in vals:
                    if member_ids:
                        rec.message_unsubscribe(member_ids)

                    team = self.env['crm.team'].search([('id', '=', vals['team_id'])])
                    if team:

                        new_memb = []
                        for memb in team.member_ids:
                            new_memb.append(memb.partner_id.id)
                        support_team = self.env['res.partner'].search(
                            [('email', '=', 'business_support_team@thehelpinghand.org.sg')])
                        if support_team:
                            new_memb.append(support_team.id)

                        rec.message_subscribe(new_memb, None)
        return res.write(vals)

    def action_confirm(self):

        res = super(SaleOrderInherit, self).action_confirm()

        if len(self.picking_ids) > 1:
            ids = []
            for picking_ids in self.picking_ids:
                ids.append(picking_ids.id)
            sorted_list = sorted(ids)

            do_pick = self.env['stock.picking'].sudo().search([('id', '=', sorted_list[-1])])

        else:
            do_pick = self.picking_ids
        if self.preferred_delivery_date:
            do_pick.write({'internal_remarks': self.internal_remarks, 'scheduled_date': self.preferred_delivery_date,
                           'date_deadline': self.preferred_delivery_date})
        else:
            do_pick.write({'internal_remarks': self.internal_remarks})
        self.write({'scheduled_delivery_date': do_pick.scheduled_date})
        return res

    def _prepare_invoice(self):
        print("=============")

        res = super(SaleOrderInherit, self)._prepare_invoice()

        vals = {
            'internal_remarks': self.internal_remarks

        }
        if self.remarks:
            vals.update({'remarks':self.remarks})
        # print(vals)
        # print("=====================================================")
        # exit()
        res.update(vals)
        return res

    def state_change(self):

        name = self.name
        if self.state == 'sale':
            name = name.replace("QO", "SO")
            self.write({'name': name})
        elif self.state == 'draft':
            name = name.replace("SO", "QO")
            self.write({'name': name})

    def _delivery_status(self):
        for rec in self:
            rec.delivery_status = ""
            if rec.picking_ids:
                if len(rec.picking_ids) > 1:
                    ids = []
                    for picking_ids in rec.picking_ids:
                        ids.append(picking_ids.id)
                    sorted_list = sorted(ids)

                    do_pick = self.env['stock.picking'].sudo().search([('id', '=', sorted_list[-1])])

                else:
                    do_pick = rec.picking_ids
                rec.delivery_status = do_pick.state
                rec.write({'delivery_status': do_pick.state})

    def _payment_status(self):
        for rec in self:
            rec.payment_status = ""
            if rec.invoice_ids:
                if len(rec.invoice_ids) > 1:
                    ids = []
                    for invoice_ids in rec.invoice_ids:
                        ids.append(invoice_ids.id)
                    sorted_list = sorted(ids)
                    do_invo = self.env['account.move'].sudo().search([('id', '=', sorted_list[-1])])

                else:
                    do_invo = rec.invoice_ids
                rec.invoice_date = do_invo.invoice_date
                rec.invoice_number = do_invo.name
                rec.payment_status = do_invo.payment_state
                rec.write({'payment_status': do_invo.payment_state, 'invoice_date': do_invo.invoice_date,
                           'invoice_number': do_invo.name})


    @api.onchange('invoice_ids')
    def _invoice_amount_paid(self):
        for rec in self:

            if rec.invoice_ids:
                total = 0.00
                for in_id in rec.invoice_ids:

                    if in_id.payment_state == 'paid':
                        total = total + in_id.amount_total
                        rec.amount_paid = total
                    else:
                        rec.amount_paid = total
            else:
                rec.amount_paid = 0.00
    def _payment_memo(self):

        for rec in self:
            rec.payment_memo = ""
            if rec.invoice_ids:

                if len(rec.invoice_ids) > 1:
                    ids = []
                    for invoice_ids in rec.invoice_ids:
                        ids.append(invoice_ids.id)
                    sorted_list = sorted(ids)

                    do_invo = self.env['account.move'].sudo().search([('id', '=', sorted_list[-1])])

                    pay_ref = do_invo.payment_reference

                    if pay_ref:
                        payment_ref = self.env['account.payment'].sudo().search([('payment_reference', '=', pay_ref)])

                        if len(payment_ref) > 1:
                            rec.payment_memo = payment_ref[-1].ref
                            rec.journal_id = payment_ref[-1].journal_id
                        else:
                            rec.payment_memo = payment_ref.ref
                            rec.journal_id = payment_ref.journal_id
                else:
                    pay_ref = rec.invoice_ids.payment_reference
                    if pay_ref:

                        payment_ref = self.env['account.payment'].sudo().search([('ref', '=', pay_ref)])

                        if len(payment_ref) > 1:
                            rec.payment_memo = payment_ref[-1].ref
                            rec.journal_id = payment_ref[-1].journal_id
                        else:
                            rec.payment_memo = payment_ref.ref
                            rec.journal_id = payment_ref.journal_id

    def _scheduled_delivery_date(self):
        for rec in self:
            delivery = rec.picking_ids
            rec.scheduled_delivery_date = ""
            if delivery:
                if rec.preferred_delivery_date:
                    delivery[-1].write(
                        {'scheduled_date': rec.preferred_delivery_date, 'date_deadline': rec.preferred_delivery_date})
                rec.scheduled_delivery_date = delivery[-1].scheduled_date



    @api.onchange('sale_order_template_id')
    def get_team_from_temp(self):
        if self.sale_order_template_team_id:

            self.team_id = self.sale_order_template_team_id

    internal_remarks = fields.Text(string='Internal Remarks')
    delivery_status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Operation')
    ], string='Delivery Status',readonly=True, compute=_delivery_status)
    payment_status = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('to_pay', 'Not Paid'),
        ('partial', ' Partially Paid'),
        ('free', 'Free'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy')
    ], string='Payment Status', readonly=True, compute=_payment_status)

    scheduled_delivery_date = fields.Datetime(string='Scheduled Delivery Date', readonly=True)
    payment_memo = fields.Char(string='Payment Memo', compute=_payment_memo)
    journal_id = fields.Many2one('account.journal', string='Journals', readonly=True)
    show_customer_info = fields.Boolean(string='Show Customer Info', default=True)
    preferred_delivery_date = fields.Datetime(string='Preferred Delivery Date', readonly=False)
    sale_order_template_categ_id = fields.Many2one(related='sale_order_template_id.product_category_id')
    sale_order_template_team_id = fields.Many2one(related='sale_order_template_id.team_id', store=True)
    myob_invoice_created = fields.Boolean(string='MYOB Invoice Created')
    myob_invoice_number = fields.Char(string='MYOB Invoice Number')
    myob_sales_order_created = fields.Boolean(string='MYOB Sales Order Created')
    myob_sales_order_number = fields.Char(string='MYOB Order Number')
    amount_paid = fields.Char(string='Amount Paid',compute=_invoice_amount_paid)
    invoice_number = fields.Char(string='Invoice Number' ,readonly=True)
    invoice_date = fields.Char(string='Invoice Date' ,readonly=True)
    remarks = fields.Text(string='Remarks')
