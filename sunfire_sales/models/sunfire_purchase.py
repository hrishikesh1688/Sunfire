from odoo import models,fields
class PurchaseOrderInhe(models.Model):
    _inherit = 'purchase.order'
    delivery_period=fields.Many2one('delivery_period.info','Delivery Period')
    warranty=fields.Many2one('warranty_information.info','Warranty')
    lead_name=fields.Many2one('lead_source_information.info','Lead Name')


class delivery_period_info(models.Model):
    _name='delivery_period.info'
    _rec_name ="delivery_period"  
    delivery_period=fields.Char('Delivery Period')
     
     
class warranty_information(models.Model):
    _name='warranty_information.info'
    _rec_name ="warranty"  
    warranty=fields.Char('Warranty')
 
class lead_source_information(models.Model):
    _name='lead_source_information.info'
    _rec_name ="lead_name"  
    lead_name=fields.Char('Lead Name')
