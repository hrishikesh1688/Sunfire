from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    @api.multi
    def cust_type_val(self):
        temp="Not Built"
        cust_type_obj=self.env['cust.type']
        cust_type_id=cust_type_obj.search([("cust_type","=",temp)])
        print("cust_type_id",cust_type_id.id)
        return cust_type_id.id

    cust_type=fields.Many2one('cust.type',string="Customer Type",default=cust_type_val)
    oem = fields.Boolean(string='Is a OEM',
                               help="Check this box if this contact is a oem. "
                               "If it's not checked, purchase people will not see it when encoding a purchase order.")
    