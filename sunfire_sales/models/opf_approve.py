from odoo import api,fields,models

# class ResPartnerInhe(models.Model):
#     _name="res.partner"
#     presales_user=fields.Many2many("res.users",string="Pre-Sales")
#     techservice_users=fields.Many2many("res.users",string="Tech-Services")
#     buh_user=fields.Many2many("res.users",string="BUH head")

class approval_type_info(models.Model):
    _name='approval_types.info'
    _rec_name='approval_type'
    approval_type=fields.Char("Type")

class approval_info(models.Model):
    _name='approval.info'
    _sql_constraints = [ ('unique_approval', 'unique(vendor,users,approval_type)', 'Approval already defined')	]
    _rec_name='users'
    vendor=fields.Many2one('res.partner')
    users=fields.Many2one('res.users')
    approval_type=fields.Many2one('approval_types.info')
   
class approval_tab_info(models.Model):
    _name='approval_tab.info'
    
    order_approve_id=fields.Many2one('sale.order', ondelete='cascade', index=True, copy=False)
    vendor=fields.Many2one('res.partner',required=True)
    users=fields.Many2one('res.users',required=True)
    approval_type=fields.Many2one('approval_types.info',required=True)
    approve_status=fields.Boolean('Approval Status')
    @api.onchange('vendor')
    def onchange_vendor(self):
        users_list=[]
        domain={}
        approve_obj = self.env['approval.info']
        con_ids=approve_obj.search([('vendor.id','=',self.vendor.id)])
        for i in con_ids:
            users_list.append(i.users.id)
        domain['users']=[('id','in',users_list)]
        return {'domain':domain}
    @api.onchange('users')
    def onchange_user(self):
        type_list=[]
        domain={}
        approval_obj = self.env['approval.info']
        co_ids=approval_obj.search([('users.id','=',self.users.id),('vendor.id','=',self.vendor.id)])
        for i in co_ids:
            type_list.append(i.approval_type.id)
        domain['approval_type']=[('id','in',type_list)]
        return {'domain':domain}

    