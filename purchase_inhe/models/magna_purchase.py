from odoo import api, fields, models

class PurchaseOrderInhe(models.Model):
    _inherit = 'purchase.order'
     
  
    margin=fields.Float(string='Margin',readonly=False)
    my_discount = fields.Float(string='Discount')
    my_total = fields.Monetary(string='Total',compute='my_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True,compute='_amount_all')

    
    @api.onchange('margin')
    def _cal_total_onchange_margin(self):
        print(self)
        if self.margin:
            
            self.amount_total = self.my_total + self.margin-self.my_discount
       
        
    @api.onchange('my_discount')
    def _cal_total_onchange_discount(self):
        print(self)
        if self.my_discount:
            # print("######Discount######dis",self.my_discount)
            # print("######Margin######dis",self.margin)
            # print('#######self.my_total#######dis befor',self.my_total)
            self.amount_total=self.my_total + self.margin-self.my_discount
            # print('#######self.amount_total#######dis',self.amount_total)
            # self._amount_all()
    @api.depends('order_line.price_total')
    def my_amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                # print("#######values########",self.margin,self.my_discount,self.amount_total)
                self.my_total=amount_untaxed
            # print("#######values########",self.margin,self.my_discount,self.amount_total)

    @api.depends('margin','my_discount','order_line.price_total','order_line.product_qty','order_line.purchase_price')  
    def _amount_all(self):
        for order in self:
            print("final123====>",self.amount_total)
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                print("AMount_untaxed=====>",amount_untaxed,self.margin,self.my_discount)
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + self.margin-self.my_discount,
            })
            print("final====>",self.amount_total)  

    #update 'NA' PO_STATE in sale.order.line after cancel purchase order 23/06/18
    @api.multi
    def button_cancel(self):
        sale_order_line_obj = self.env['sale.order.line']
        for order in self:
            if order.state in ('draft', 'purchase'):
                for order_line in order.order_line:
                    print('SOL Id--------',order_line.saleorder_line_id.id)
                    sale_orde_line_rec = sale_order_line_obj.search([('id','=',order_line.saleorder_line_id.id)])
                    if sale_orde_line_rec:
                        sale_orde_line_rec.write({'id':order_line.saleorder_line_id.id,'po_state':'NA'})
                        print('success NA')
            for pick in order.picking_ids.filtered(lambda r: r.state != 'cancel'):
                pick.action_cancel()

        self.write({'state': 'cancel'})
       

