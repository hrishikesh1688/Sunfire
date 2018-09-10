from odoo import api, fields, models


class revision_order(models.Model):
    _inherit = 'sale.order'
    _name='revision.order'

    quotation_id=fields.Many2one('sale.order',string="Quotation Id")
class revision_order_line(models.Model):
    _inherit='sale.order.line'
    _name='revision.order.line'

        
