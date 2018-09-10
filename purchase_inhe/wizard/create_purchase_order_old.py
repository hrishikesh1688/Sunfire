from openerp import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
import requests

class sale_order_line_inhe(models.Model):
    _inherit = 'sale.order.line'   
    #Added PO_STATE field in sale order line table 18/06/18
    po_state = fields.Char(string='PO state',invisible=True,default='NA')
    purchaseorder_line_id=fields.One2many('purchase.order.line','saleorder_line_id',string='purchaseorder_line_id')
   
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'   

    #new added desc_name,saleorder_line_id in purchase order line 15/06/2018
    desc_name=fields.Text(related='product_id.description_sale',string='Description')
    saleorder_line_id=fields.Many2one('sale.order.line',string='sale line ID')

    @api.onchange('product_qty')
    def _onchange_product_qty(self):

        #print('PO innnnn ----------')
        purchase_order_line_obj = self.env['purchase.order.line']
        my_purchase_obj=self.env['purchase.order']
        sale_order_line_data = self.env['sale.order.line']
        qtysum = 0
        sol = 0
        changeqty = self.product_qty
        #print("changeqty",changeqty)
        #print("SOL id------------->",self.saleorder_line_id.id)
      
        purchase_order_line_Qty=purchase_order_line_obj.search([('saleorder_line_id','=',self.saleorder_line_id.id),('state', '!=', 'cancel')])
        for qty in purchase_order_line_Qty:
            qtysum += qty.product_qty    

        saleorderlinedata = sale_order_line_data.search([('id','=',self.saleorder_line_id.id)])
        print('sale order qty---',saleorderlinedata.product_uom_qty)
        if saleorderlinedata.product_uom_qty != 0 or changeqty==0 :

            if saleorderlinedata.product_uom_qty < changeqty :
                raise UserError(_('Can not enter less then product qty'))

            remqty = saleorderlinedata.product_uom_qty - (qtysum-changeqty)
            #print('saleqty--',saleorderlinedata.product_uom_qty,'remain--',remqty,' sum--',qtysum,'change qty',changeqty)  
            if remqty < changeqty:
                raise UserError(_('Can not enter more then %d remain qty') %(remqty))

            if changeqty == 0:
                raise UserError(_('Can not enter 0 qty'))       
   
    @api.model
    def write(self, values):
        
        sale_order_line_obj = self.env['sale.order.line']
        purchase_order_line_obj = self.env['purchase.order.line']

        result = super(PurchaseOrderLine, self).write(values)
        for line in self:
            #Get purchase qty sum on sale order line item
            #print('line id--',line.saleorder_line_id.id)      
            purchase_order_line_Qty=purchase_order_line_obj.search([('saleorder_line_id','=',line.saleorder_line_id.id),('state', '!=', 'cancel')])
            Sum = 0
            for qty in purchase_order_line_Qty:
                Sum += qty.product_qty
            print('Tot Qty---------',Sum,'line id--',line.saleorder_line_id.id)        
            sale_orde_line_rec = sale_order_line_obj.search([('id','=',line.saleorder_line_id.id)])
            #update state in sale order line as 'NA' if QTY not Match else update 'PO confirm'
            if Sum != sale_orde_line_rec.product_uom_qty:               
                sale_orde_line_rec.write({'id':line.saleorder_line_id.id,'po_state':'NA'})
            else:
                sale_orde_line_rec.write({'id':line.saleorder_line_id.id,'po_state':'PO confirm'}) 
    
    #update sale order line item PO state NA witch is deleted from purchase order 15/06/18
    @api.multi
    def unlink(self):
        sale_order_line_obj = self.env['sale.order.line']    
        
        for line in self:
            print('-------------------deleted id :',line.saleorder_line_id.id)
            tempid=line.saleorder_line_id.id
            self.env.cr.execute("update sale_order_line set po_state='NA' where id= %s",(tempid,))            
            #sale_order_line_obj.write({'id':line.saleorder_line_id.id,'po_state':'NA2'})
            if line.order_id.state in ['done']:
                raise UserError(_('Can not delete a purchase order line which is in state \'%s\'.') %(line.state,))
        return super(PurchaseOrderLine, self).unlink()

    
class CreatePurchaseOrder(models.Model):

    #update status created by,date and updated by,date in table
    _name='create.purchase.order' 
    
    order_id = 0
    @api.multi
    def call_purchase_order(self):
        sale_order_obj = self.env['sale.order']
        sale_order_line_obj = self.env['sale.order.line']
        purchase_order_obj = self.env['purchase.order']
        purchase_order_line_obj = self.env['purchase.order.line']
        dr_data_info_obj = self.env['dr_data.info']
        res_partner_obj = self.env['res.partner']
        po_order={}
        po_line = {}
        now = datetime.datetime.now()
        count = 0    
        opf_no=''
        opf_no_ary =[]

        active_ids = self.env.context['active_ids']
        for id in active_ids:
            sale_orde_line_rec = sale_order_line_obj.search([('order_id','=',id),('po_state','=','NA')])
            #print('so id------',sale_orde_line_rec.id)          
            for soid in sale_orde_line_rec:
                count += 1

            sale_order_rec = sale_order_obj.search([('id','=',id)])
            opf_no_ary.append(sale_order_rec.opf_name)
            #print('opf no list -------------',sale_order_rec.opf_name)
            partnerid = dr_data_info_obj.search([('order_dr_id','=',id)])
            print('partnerid -------------',partnerid.vendor_dr_id.id)
        
        partner_invoice_id = res_partner_obj.search([('parent_id','=',partnerid.vendor_dr_id.id),('type','=','invoice')])
        print('partner_invoice_id 1-------------',partner_invoice_id.id)
        if partner_invoice_id.id == False:
            partner_invoice_id = res_partner_obj.search([('id','=',partnerid.vendor_dr_id.id),('type','=','contact')])
            print('partner_invoice_id 2-------------',partner_invoice_id.id)
       

        #print('opf list -------------',opf_no_ary)
        opf_no = ",".join(str(s) for s in opf_no_ary)
        #print('OPF NO --------------------',opf_no)        
         
        if count == 0 :
            raise UserError(_("PO already processed"))
        else:           
            po_order= {
                        'partner_id':partnerid.vendor_dr_id.id,
                        'date_order':now.strftime('%Y-%m-%d'), 
                        'partner_invoice_id':partner_invoice_id.id,
                        'partner_shipping_id':partner_invoice_id.id,
                        'origin':opf_no,                    
            }
            purchase_order_id=purchase_order_obj.create(po_order)
            #order_id = purchase_order_id.id
        for active_id in active_ids:

            sale_order_rec = sale_order_obj.search([('id','=',active_id)])
            sale_orde_line_rec = sale_order_line_obj.search([('order_id','=',active_id),('po_state','=','NA')])
          
            if sale_order_rec.state == 'done':    
                for line in sale_orde_line_rec:                                     
                    if line.po_state == 'NA':
                        po_line = {
                            'order_id':purchase_order_id.id,
                            'date_planned': now.strftime('%Y-%m-%d'),
                            'name':line.product_id.description_sale,
                            'product_id': line.product_id.id,
                            'product_qty': line.product_uom_qty,
                            'product_uom': line.product_uom.id,
                            'price_unit': line.price_unit,
                            'price_subtotal': line.price_subtotal,                            
                            'saleorder_line_id':line.id,
                            'purchase_price':line.purchase_price,
                            'layout_category_id':line.layout_category_id.id,                                           
                        }

                    #print('id---------',line.id,line.po_state)
                    purchase_line_id=purchase_order_line_obj.create(po_line) 
                # update state in sale order line as confirm
                sale_orde_line_rec.write({'id':line.id,'po_state':'PO confirm'}) 
                view = self.env.ref('purchase.purchase_order_form')
                ctx=dict(self.env.context)          
            else:
                raise UserError(_("Only locked state order will be processed"))        
        return {
                    'name': 'Purchase Order',
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'purchase.order',
                    'res_id': purchase_order_id.id,
                    'views': [(view.id, 'form')],
                    'target': 'new',
                    'context': ctx,
                }

   
   
