from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class stock_move_inhe(models.Model):
    _inherit = 'stock.move'
    #Validation for received qty and entered qty
    @api.onchange('quantity_done')
    def _onchange_quantity_done(self):
       
        doneqty = self.quantity_done
        print('-------Done qty---',doneqty)
        recvqty = self.product_uom_qty
        print('-------Recv qty---',recvqty)

        if recvqty < doneqty:
            raise UserError(_('Can not enter more then %d qty') %(recvqty,))

