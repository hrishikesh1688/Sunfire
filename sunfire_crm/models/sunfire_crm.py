from odoo import api, fields, models
from datetime import datetime

class SunfireCrm(models.Model):
    _inherit = 'crm.lead'
    shrt_name=fields.Char("Short Name",size=150)
    partner_id = fields.Many2one('res.partner', string='Customer', track_visibility='onchange',required=True, index=True,help="Linked partner (optional). Usually created when converting the lead.")
    priority = fields.Selection(string='Key Deal', selection=[('Yes', 'Yes'), ('No', 'No'),],default='Yes')
    inside_sales=fields.Many2one('approval.info')
    # inside_sales=fields.Selection("inside_sales_vals","Inside Sales")
    planned_revenue = fields.Float('Expected Revenue (TL)', track_visibility='always')
    bottom_line_revenue=fields.Float('Expected Revenue (BL)', track_visibility='always')
    deal_type=fields.Many2one('deal_type.info')
    oem2=fields.Many2one('res.partner',string='Vendor')
    dr_lines=fields.One2many('dr_data.info', 'crm_order_dr_id', string='Order Lines',copy=True, auto_join=True)
    date_deadline_mnth=fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                          (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), 
                          (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')],'Expected closing (Month)')
    date_deadline_year=fields.Selection([(num, str(num)) for num in range(2018, (datetime.now().year)+8 )],'Expected Closing (Year)')
    crm_pricelist_id=fields.Many2one('product.pricelist',string="Revenue Type",required=True)
    opportunity_stages=fields.Many2one('opportunity_stages.info')
    sales_stages=fields.Many2one('sales_stages.info') 
    crm_line=fields.One2many('sale.order','opportunity_id')
    quotation_name=fields.Char(related="crm_line.name",string="Quotation Number")
    @api.multi
    def inside_sales_vals(self):
        appr_vals=[]
        abc=[]
        domain={}
        approval_obj=self.env['approval.info']
        inside_sales_ids=approval_obj.search([('approval_type','=','Inside Sales')])
        #print(inside_sales_ids)
        for i in inside_sales_ids:
            #print("ids and users====================>",i.id,i.users.name)
            appr_vals.append((i.users.id,i.users.name))
        abc=appr_vals
        return appr_vals

    

    @api.multi
    def sale_action_quotations_new(self):
        sale_order_obj=self.env['sale.order']
        res_partner_obj=self.env['res.partner']
        print("self.stage_id.name",self.stage_id.name)
        print("Quotation name",self.crm_line.name)
        so_order= {
                    'opportunity_stages':self.opportunity_stages.id,
                    'sales_stages':self.sales_stages.id,
                    'partner_id':self.partner_id.id,
                    'partner_invoice_id':self.partner_id.id,
                    'partner_shipping_id':self.partner_id.id, 
                    'pricelist_id':self.crm_pricelist_id.id,
                    'opportunity_id':self.id,
                    'shrt_name':self.shrt_name             
            }
        sale_order_obj_id=sale_order_obj.create(so_order)
        print(sale_order_obj_id.id)
        for i in self:
            for ids in i.dr_lines:
                ids.order_dr_id=sale_order_obj_id.id                
        view = self.env.ref('sale.view_order_form')
        ctx=dict(self.env.context)
        stage=self.env['crm.stage'].search([('name','=','Quotation')])
        print(stage)
        self.stage_id=stage.id
        return {
        'name': 'Quotation',
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'sale.order',
        'res_id':sale_order_obj_id.id,
        'views': [(view.id, 'form')],
        'target': 'new',
        'context': ctx,
    }

    

class crm_dr_info(models.Model):
    _inherit='dr_data.info' 
    
    crm_order_dr_id = fields.Many2one('crm.lead', string='Order DR Reference', ondelete='cascade', index=True, copy=False)

class stages_info(models.Model):
    _name="stages.info"
    stages_line_id=fields.Many2one('crm.lead',ondelete='cascade', index=True, copy=False)
    sales_stages=fields.Many2one('sales_stages.info')
    opportunity_status=fields.Many2one('opportunity_stages.info')




















    

    
    