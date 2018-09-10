from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from datetime import datetime


class purchase_inhe(models.Model):
    _inherit = 'purchase.order'

   
    partner_id = fields.Many2one('res.partner', string='Supplier Name', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    # new Added partner_invoice_id
    partner_invoice_id = fields.Many2one('res.partner',string='Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Invoice address for current Purchase order.")
    # new Added partner_shipping_id
    partner_shipping_id = fields.Many2one('res.partner', string='Ship. To',readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current Purchase order.",)
    partner_invoice_Add=fields.Text("Address Detail",readonly=True)
    partner_shipping_Add=fields.Text("Shipping Street",readonly=True)
    other_address_check=fields.Boolean("",default=False,help="Check this box for create other address")
    other_address=fields.Text(readonly=True,default='NA')    

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    partner_ref = fields.Char('Kind Attention', copy=False,\
        help="Reference of the sales order or bid sent by the vendor. "
             "It's used to do the matching when you receive the "
             "products as this reference is usually written on the "
             "delivery order sent by your vendor.")

    date_order = fields.Datetime('PO Date', required=True, states=READONLY_STATES, index=True, copy=False, default=fields.Datetime.now,\
        help="Depicts the date where the Quotation should be validated and converted into a purchase order.")
    
    tax_grp = fields.Many2one('account.tax',string="Tax Group")

    po_to_be_placed=fields.Many2one('res.partner',string="Shipping Address")
    po_detail_address=fields.Many2one('res.partner',string="Billing Address")
    
    #Create by : Ganesh Date : 13/07/18
    #PO Sequence no generate on month wise
    @api.model
    def create(self, vals):
        '''
        This Function return custome sequence no on month wise
        '''
        if vals.get('name', 'New') == 'New':
            currentMonth = datetime.now().strftime('%m')
            print ('Current months-------',currentMonth)
            
            if currentMonth=='11':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'A') or '/'
            elif currentMonth=='12':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'B') or '/'
            elif currentMonth=='01':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'C') or '/'
            elif currentMonth=='02':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'D') or '/' 
            elif currentMonth=='03':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'E') or '/'       
            elif currentMonth=='04':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'F') or '/'
            elif currentMonth=='05':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'G') or '/'
            elif currentMonth=='06':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'H') or '/'
            elif currentMonth=='07':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'I') or '/'
            elif currentMonth=='08':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'J') or '/'
            elif currentMonth=='09':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'K') or '/'
            elif currentMonth=='10':
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order').replace('X', 'L') or '/'              
        return super(purchase_inhe, self).create(vals)

    @api.onchange('po_detail_address')
    def _company_addr(self):     
        '''
        This Function use to show company address of all
        '''   
        con=[]
        domain={}
        res_company_obj = self.env['res.partner']
        con_ids=res_company_obj.search([('parent_id','=',1)])
        for i in con_ids:
            con.append(i.id)
        domain['po_to_be_placed']=[('id','in',con)]
        domain['po_detail_address']=[('id','in',con)]
        print('-----------',domain)
        return {'domain':domain}   
   
    #Pradeep Code merge 29/06/18
    #code start     
    @api.multi
    @api.onchange('partner_id') 
    def onchange_partner_id(self):
        '''
        This Function is use to bind partner invoice and partner shipping address
        '''
        partners_invoice = []
        partners_shipping = []
        domain = {}
        for record in self:
            if record.partner_id:
                for part in record.partner_id:
                    partners_invoice.append(part.id)
                    partners_shipping.append(part.id)
                    if record.partner_id.child_ids:
                        for partner in record.partner_id.child_ids:
                            # if partner.type == 'invoice':
                            partners_invoice.append(partner.id)
                            # if partner.type == 'delivery':
                            partners_shipping.append(partner.id)
                    if partners_invoice:
                        domain['partner_invoice_id'] =  [('id', 'in', partners_invoice)]
                    else:
                        domain['partner_invoice_id'] =  []
                    if partners_shipping:
                        domain['partner_shipping_id'] = [('id', 'in', partners_shipping)]
                        print("print6666666666666666",partners_invoice)
                    else:
                        domain['partner_shipping_id'] =  []
            else:
                domain['partner_invoice_id'] =  [('type', '=', 'invoice')]
                print("print7777777777777777",partners_invoice)
                domain['partner_shipping_id'] =  [('type', '=', 'delivery')]
                print("print88888888888888",partners_invoice)
        return {'domain': domain}
    #code End           
   
    # @api.onchange('partner_invoice_id','partner_shipping_id')
    # def onchange_partner__invoice(self):
    #     self.partner_invoice_Add=self.partner_invoice_id.street

    # @api.onchange('partner_invoice_id','partner_shipping_id')
    # def onchange_partner__shipping(self):
    #     self.partner_shipping_Add=self.partner_shipping_id.street
    
    #Pradip Code start 20/08/18
    @api.onchange('partner_invoice_id')
    def onchange_partner__invoice(self):
         self.partner_invoice_Add = '%s %s %s %s %s %s' %(self.partner_invoice_id.street or '' , 
         self.partner_invoice_id.street2 or '', self.partner_invoice_id.city or '', 
         self.partner_invoice_id.state_id.name or '', 
         self.partner_invoice_id.zip or '', self.partner_invoice_id.country_id.name or '')
    
    #end
        
class purchase_line_inhe(models.Model):
    _inherit = 'purchase.order.line'       

    #new added line in order line
    purchase_price = fields.Float(string='Buying Price', digits=dp.get_precision('Product Price'))
    price_unit = fields.Float(string='Unit Price', required=False, digits=dp.get_precision('Product Price'))
    product_id = fields.Many2one('product.product', string='Product', domain=[('purchase_ok', '=', True)], change_default=True, required=True)
    date_planned = fields.Datetime(string='Scheduled Date', required=True, index=True)
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True,readonly=True)
    layout_category_id = fields.Many2one('sale.layout_category', string='Section')

    @api.depends('product_qty', 'price_unit', 'taxes_id','purchase_price')
    def _compute_amount(self):
        '''
        This function is inherit for calculate price_subtotal,price_total on purchase_price
        '''
        for line in self:
            taxes = line.taxes_id.compute_all(line.purchase_price, line.order_id.currency_id, line.product_qty, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
