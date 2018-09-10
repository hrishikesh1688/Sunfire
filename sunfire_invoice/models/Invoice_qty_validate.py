from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons import decimal_precision as dp

class account_invoice_inhe(models.Model):
    _inherit = 'account.invoice.line'


    #opf_name = ields.Text(string='OPF Name', required=True,readonly=True)
    l10n_in_hsn_code = fields.Char(related='product_id.l10n_in_hsn_code',string="HSN Code")
    # hsn_code = fields.Char(related='l10n_in_hsn_code',string="HSN Code") 
    name = fields.Text(string='Description', required=True,readonly=True)
    price_subtotal = fields.Monetary(string='Amount',store=True, readonly=True, compute='_compute_price', help="Total amount without taxes")
    
    #Validation for received qty and entered qty
    @api.onchange('quantity')
    def _onchange_quantity_done(self):
        purqtysum =0
        invqtysum=0
        remqty=0

        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        account_invoice_line_obj = self.env['account.invoice.line']
        purchase_order_line_obj = self.env['purchase.order.line']

        #Get qty from sale order line
        sale_order_data=sale_order_obj.search([('name','=',self.origin)])
        print('SO ID--------------',sale_order_data.id)
        sale_order_line_data = sale_order_line_obj.search([('order_id','=',sale_order_data.id),('product_id','=',self.product_id.id)])
      
        #Get qty from account invoice line 
        account_invoice_line_data = account_invoice_line_obj.search([('origin','=',self.origin),('product_id','=',self.product_id.id)])
        for line in  account_invoice_line_data:
            invqtysum += line.quantity
      
        #print('invoice sum qty----',invqtysum)
        for line in  sale_order_line_data:
            remqty = line.qty_delivered - invqtysum
        #print('remain qty---------',remqty)
        if remqty < 0 :
            raise UserError(_('Can not enter more then received quantity'))
        # if remqty < self.quantity:
        #     raise UserError(_('Can not enter more then %d remain qty') %(remqty))       


class account_invoice_eway(models.Model):
    _inherit = 'account.invoice'  

    transmode = fields.Selection([('1','Road'),('2','Rail'),('3','Air'),('4','Ship')],required=True)
    transdistance = fields.Char(string='Distance (km)',required=True)
    transportername = fields.Char(string='Transporter Name')
    transporterid = fields.Char(string='Transporter ID')
    transdocno = fields.Char(string='Document No.')   
    vehicleno = fields.Char(string='Vehicle No.')
    vehicletype = fields.Selection([('R','Regular'),('O','ODC')])
    transdocdate = fields.Date(string='Transaction doc. date',index=True,help="Transaction date should be greater then invoice date", copy=False)
    

    

   





        

        
