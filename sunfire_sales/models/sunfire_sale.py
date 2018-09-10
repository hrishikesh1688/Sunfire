from odoo import api,fields,models, _
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from odoo.exceptions import UserError
import smtplib
from ftplib import FTP
#Model Group Code 
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    # model_group_code = fields.Char('Model Group Code')
    #l10n_in_hsn_code = fields.Char(string="HSN/SAC Code", help="Harmonized System Nomenclature/Services Accounting Code")
    
#Extra fields added to SaleOrderLine 
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    i_type = fields.Selection(related='product_id.type',string='Product Type')
    desc_name=fields.Text(related='product_id.description_sale',string='Description')
    # model_group_code = fields.Char(related='product_id.model_group_code',string='Model Group Code')
    categ_id = fields.Many2one(related='product_id.categ_id',string='Product Category')
    l10n_in_hsn_code = fields.Char(related='product_id.l10n_in_hsn_code',string="HSN Code")
    dr_done = fields.Selection([('DR Done', 'DR Done'), ('DR Not Done', 'DR Not Done'),('DR Not Required','DR Not Required')], 'DR Done')
    dr_status = fields.Selection([('Accepted', 'Accepted'), ('Rejected', 'Rejected')], 'DR Status')
    dr_remark = fields.Char('DR Number')
    dr_date = fields.Char('DR Date')
    up_sell=fields.Selection([('No','No'),('Yes','Yes')],'Up Sell',default='No') 
    margin_type = fields.Selection([('Fixed', '₹'), ('Percentage', '%')], 'Margin Type')
    margin_value = fields.Float('Margin Amount')
    product_id = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)], change_default=True, ondelete='restrict', required=False)
    line_of_business=fields.Many2one('line_of_business.info',string='Line of Business')
    product_serial_no = fields.Char(string='product_serial_no')

    
    # ____________-------Margin Calculations------------__________________#
    @api.multi
    @api.onchange('margin_value','margin_type','purchase_price')
    def _my_compute_margin(self):
        for line in self:
            mt=line.margin_type
            if mt=='Percentage':
                line.price_unit=(line.purchase_price + (line.purchase_price * (line.margin_value/100)))
            else:
                line.price_unit=line.purchase_price + line.margin_value
    #_______________-------list for values top be updated------______________#
    def _get_protected_fields(self):
        return [
            'product_id', 'name', 'price_unit', 'product_uom', 'product_uom_qty',
            'tax_id', 'analytic_tag_ids','l10n_in_hsn_code'
        ]

    

    
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _sql_constraints = [ ('unique_opportunity', 'unique(opportunity_id)', 'Quotation exists')	]
    shrt_name=fields.Char("Short Name",size=150)
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    opportunity_stages=fields.Many2one('opportunity_stages.info')
    sales_stages=fields.Many2one('sales_stages.info')
    installation_terms=fields.Many2one('installation_terms.info')
    delivery_terms = fields.Many2one('delivery_term.info','Delivery Term')    
    tax_grp = fields.Many2one('account.tax',string="Tax Group")
    transport_modes = fields.Many2one('transport_mode.info',string="Transport Modes")
    validity_dt=fields.Char()
    po_to_be_placed=fields.Many2one('res.partner',string="PO to be Placed")
    po_detail_address=fields.Many2one('res.partner',string="PO addresses",help="Contact Person ")
    addr=fields.Text("Address",readonly=True)
    pre_sale_engaged = fields.Selection([('NA','NA'),('Niranjan Subhash Ghodke','Niranjan Subhash Ghodke'),('Shivaji  Ningappa Dhanagar','Shivaji  Ningappa Dhanagar'),('Ashok Nivrutti Gavhane','Ashok Nivrutti Gavhane'),('Balkrushna Vasudev Tambe','Balkrushna Vasudev Tambe'),('Rajendra Gajendra Raut','Rajendra Gajendra Raut'),('Jitesh Shantaram Mahajan','Jitesh Shantaram Mahajan')])
    billing_location=fields.Char("Billing Location")
    invoice_advice=fields.Char("Invoice Advice")
    po_advice=fields.Char("PO Advice")
    vendor_id=fields.Many2one("res.partner",string="Billing from")
    concern_person=fields.Many2one("res.partner")
    concern_email=fields.Char()
    concern_mobile=fields.Char()
    warranty=fields.Many2one('warranty_information.info','Warranty')
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, index=True, track_visibility='always')
    partner_invoice_id = fields.Many2one('res.partner', string='Invoice Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Invoice address for current sales order.")
    partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Delivery address for current sales order.")
    partner_invoice_Add=fields.Text("Detail Address",readonly=True)
    partner_shipping_Add=fields.Text("Detail Address",readonly=True)
    opf_name = fields.Char('OPF Number')
    order_dr_line = fields.One2many('dr_data.info', 'order_dr_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    revise_quote=fields.Selection([('yes','Yes'),('no','No')],'Revise Quotation')
    revision_no=fields.Integer(default=0)
    revision_name=fields.Char()
    order_approve_line=fields.One2many("approval_tab.info","order_approve_id", states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True, auto_join=True)
    order_upload_line=fields.One2many("upload_tab.info","order_upload_id")
    # @api.multi
    # def write(self,values):
    #     if 'revise_quote' in values:
    #         if values['revise_quote']=='yes':
    #             revision_no= self.env['ir.sequence'].next_by_code('revision.number')
    #             self.revision_name=revision_no
    #             values['revise_quote']='no'
    #     result = super(SaleOrder, self).write(values)
    #     return result
    
    



    @api.model
    def create(self,values):
        #print("self=========>self",self)
        #self.approval_tab_validation(values)
        rev_obj=self.env['revision.order']
        res_part_obj=self.env['res.partner']
        cust_type_obj=self.env['cust.type']
        cust_type_id=cust_type_obj.search([("cust_type","=","New")])
        res_part_id=res_part_obj.search([("id","=",values['partner_id'])])
        # print("debug1============",res_part_id)
        # print("debug2============",res_part_id.cust_type)
        # print("debug3============",cust_type_id.id)
        if res_part_id.cust_type.cust_type=="Not Build":
            res_part_id.cust_type=cust_type_id.id
            #print("debug45============",res_part_id.cust_type.cust_type)
        line = super(SaleOrder, self).create(values)
        
        #print("AAAAAAAAAAAAABBBBBBBBBBBBB",values,values['quotation_id'])
        #line_rev=super(SaleOrder,rev_obj).create(values)
        return line

    @api.multi
    def action_done(self):
        for order in self:
            if order.order_approve_line:
                for ids in order.order_approve_line:
                    if ids.approve_status==False:
                        raise models.ValidationError('Cannot approve.Approvals pending.')
                    else:
                        self.write({'state': 'done'}) 
            else:
                self.write({'state':'done'})




    '''approval stages sets approval status as done for
    user against whom approval is assigned'''
    @api.multi
    def approve_opf(self):
        for order in self:
            if order.order_approve_line:
                for ids in order.order_approve_line:
                    #print(ids.users)
                    if ids.users.id==self.env.uid:
                        #print("I m in",ids.approve_status)
                        ids.approve_status=True

    
    
    @api.multi
    def write(self,values):
        rev_obj=self.env['revision.order']
        sale_order_obj=self.env['sale.order']
        sale_order_line_obj=self.env['sale.order.line']
        if 'revise_quote' in values:
            if values['revise_quote'] =='yes':
                self.revision_no=self.revision_no + 1
                self.revision_name="V-" + (str(self.revision_no))
                # self.revision_name=(str(self.name))+"-"+(str(self.revision_no))
                #print(self.revision_no)
                values['revise_quote']='no'
        if 'opportunity_stages' in values or 'sales_stages' in values:           
            crm_obj=self.env['crm.lead']
            #print("======================================+++++++>",self.opportunity_id)
            if self.opportunity_id.id!=False:
                crm_id=crm_obj.search([('id','=',self.opportunity_id.id)])
                #print("opportunity_stages1",crm_id.opportunity_stages)
                crm_id.opportunity_stages=values["opportunity_stages"]
                crm_id.sales_stages=values["sales_stages"]
        #print("EDIT values",values)
        if 'shrt_name' in values:
            crm_obj=self.env['crm.lead']
            if self.opportunity_id.id!=False:
                crm_id=crm_obj.search([('id','=',self.opportunity_id.id)])
                crm_id.shrt_name=values["shrt_name"]
        result = super(SaleOrder, self).write(values)
        # order_ids=rev_obj.search([('name','=',self.name)])
        # for order_ids in values['order_line']:
        #     print(order_ids)
        # values['quotation_id']=self.id
        # result_rev = super(SaleOrder, rev_obj).write(values)
        # print("RESULT=============++>",values['message_follower_ids'],values['quotation_id'],self.id)
        return result

    def approval_mail(self):
        mail_details=self.env['ir.mail_server']
        server=mail_details.search([("name","=","new Server")])
        approval_list=[]
        for order in self:
            for ids in order.order_approve_line:
                approval_list.append(ids.users)
        #print('approval_list smtp host and port=============>',approval_list,server.smtp_host,server.smtp_port)
        content='Please approve OPF no.'+self.opf_name
        mail=smtplib.SMTP(server.smtp_host,server.smtp_port)
        mail.ehlo()
        mail.starttls()
        #print("SMTP User and Password==========>",server.smtp_user,server.smtp_pass)
        mail.login(server.smtp_user,server.smtp_pass)
        for i in approval_list:
            mail.sendmail(server.smtp_user,i.login,content)
        mail.quit()
    #___________-------------Validation for DR Done------___________#
    def dr_validation(self):
        for order in self:
            if order.order_dr_line:
                for i in order.order_dr_line:
                    if i.dr_done=="DR Done":
                        if i.dr_remark==False or i.dr_date==False:
                            raise UserError(_("Dr Date or Dr Remark missing"))
            else:
                raise UserError(_("Distributor must be specified"))
    def order_info_validation(self):
        for order in self:
            if order.billing_location==False:
                raise UserError(_("Billing Location should not be Empty"))
            if order.client_order_ref==False:
                raise UserError(_("Customer PO and Dt. should not be Empty"))
            if (order.payment_term_id.id==False):
                raise UserError(_("Credit Terms should not be Empty"))
            if order.partner_id.vat==False:
                raise UserError(_("GSTIN should not be Empty"))
    @api.multi
    def action_confirm(self):
        self._action_confirm()
        res_part_obj=self.env['res.partner']
        cust_type_obj=self.env['cust.type']
        #___________-------------Validation for DR Done------___________#
        self.dr_validation()
        #____________----------validation for billing_location,client_order_ref,payment_term_id,vat-----________#
        self.order_info_validation()
        #_________________---------Changing Type of Customer from New or Not Build to Retention----__________#
        cust_type_id=cust_type_obj.search([("cust_type","=","Retention")])
        res_part_id=res_part_obj.search([("id","=",self.partner_id.id)])
        if res_part_id.cust_type.cust_type=="Not Build" or res_part_id.cust_type.cust_type=="New":
            res_part_id.cust_type=cust_type_id.id
        #____________---------Genration of OPF sequence-------____________#
        opf_seq= self.env['ir.sequence'].next_by_code('sale.order123')
        self.opf_name=opf_seq
        #___________---------On create send mail to approval list
        #self.approval_mail()
        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
            self.action_done()
        return True
    
    

    
    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
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
                            if partner.type != 'contact':
                                partners_invoice.append(partner.id)
                            if partner.type != 'contact':
                                partners_shipping.append(partner.id)
                    if partners_invoice:
                        domain['partner_invoice_id'] =  [('id', 'in', partners_invoice)]
                    else:
                        domain['partner_invoice_id'] =  []
                    if partners_shipping:
                        domain['partner_shipping_id'] = [('id', 'in', partners_shipping)]
                        #print("print6666666666666666",partners_invoice)
                    else:
                        domain['partner_shipping_id'] =  []
            else:
                domain['partner_invoice_id'] =  [('type', '=', 'invoice')]
                #print("print7777777777777777",partners_invoice)
                domain['partner_shipping_id'] =  [('type', '=', 'delivery')]
                #print("print88888888888888",partners_invoice)
        return {'domain': domain}
               
    @api.onchange('partner_invoice_id','partner_shipping_id')
    def onchange_partner__invoice(self):
        self.partner_invoice_Add = '%s %s %s %s %s %s' %(self.partner_invoice_id.street or '' , self.partner_invoice_id.street2 or '', self.partner_invoice_id.city or '', self.partner_invoice_id.state_id.name or '', self.partner_invoice_id.zip or '', self.partner_invoice_id.country_id.name or '')
                
    @api.onchange('partner_invoice_id','partner_shipping_id')
    def onchange_partner__shipping(self):
        self.partner_shipping_Add = '%s %s %s %s %s %s' %(self.partner_shipping_id.street or '' , self.partner_shipping_id.street2 or '', self.partner_shipping_id.city or '', self.partner_shipping_id.state_id.name or '', self.partner_shipping_id.zip or '', self.partner_shipping_id.country_id.name or '')
    
    @api.multi
    def open_import_product_list(self):
        view = self.env.ref('sunfire_sales.import_product_data_view_123')
        return {
            'name': 'Import Product Data',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'magna.import',       
            'views': [(view.id, 'form')],           
            'target': 'new',
        }
    
    
    @api.onchange('po_to_be_placed')
    def company_addr(self):
        #print("Eureka#1",self)
        con=[]
        domain={}
        res_company_obj = self.env['res.partner']
        con_ids=res_company_obj.search([('parent_id','=',self.po_to_be_placed.id)])
        for i in con_ids:
            con.append(i.id)
        domain['po_detail_address']=[('id','in',con)]
        #print(domain)
        return {'domain':domain}
    
    
    @api.onchange('po_detail_address')
    def _company_full_addr(self):
        self.addr=self.po_detail_address.city

    
    
    @api.multi
    def action_unlock(self):
        for line in self:
            if line.order_line:
                for ids in line.order_line:
                    #print("#####action_unlock oid",myid.id,myid.po_state)
                    if ids.po_state == "NA":
                        self.write({'state': 'sale'})
                    else:
                        raise UserError(_('You can not Unlock untill PO is canceled'))
            else:
                self.write({'state','sale'})
    
    @api.onchange('partner_id')
    def _concern_person(self):
        #print("Partner_id",self.partner_id)
        res_partner_obj = self.env['res.partner']
        concern=[]
        domain={}
        concern_ids=res_partner_obj.search([('parent_id','=',self.partner_id.id)])
        for i in concern_ids:
            #print("concern_ids",i.id)
            concern.append(i.id)
        #print("concern",concern)
        domain['concern_person']=[('id','in',concern)]
        return {'domain':domain} 
            
    @api.onchange('concern_person')
    def _concern_details(self):
        #print("Concer Person",self.concern_person)
        self.concern_mobile=self.concern_person.mobile
        self.concern_email=self.concern_person.email
   
class delivery_term_info(models.Model):
    _name='delivery_term.info'
    _rec_name ="delivery_terms"  
    delivery_terms=fields.Char('Delivery Term')

class transport_mode_info(models.Model):
    _name = 'transport_mode.info'
    _rec_name = 'transport_modes'
    transport_modes =  fields.Char('Transport Modes')
class line_of_business_info(models.Model):
    _name = 'line_of_business.info'
    _rec_name = 'line_of_business'
    line_of_business =  fields.Char('Line of Business')
class installation_terms_info(models.Model):
    _name = 'installation_terms.info'
    _rec_name = 'installation_terms'
    installation_terms = fields.Char('Installation Terms')
class sales_stages_info(models.Model):
    _name = 'sales_stages.info'
    _rec_name = 'sales_stages'
    sales_stages = fields.Char('Sales Stages')
class opportunity_stages_info(models.Model):
    _name = 'opportunity_stages.info'
    _rec_name = 'opportunity_stages'
    opportunity_stages = fields.Char('Opportunity Stages')
class cust_type(models.Model):
    _name = 'cust.type'
    _rec_name = 'cust_type'
    cust_type = fields.Char('Customer Type')
#saleOrderLine alike tab for DR info
class dr_data_info(models.Model):
    _name="dr_data.info"
    order_dr_id = fields.Many2one('sale.order', string='Order DR Reference', ondelete='cascade', index=True, copy=False)
    #oem=fields.Many2one('oem.info')
    oem1=fields.Many2one('res.partner',string='Vendor')
    dr_done = fields.Selection([('DR Done', 'DR Done'), ('DR Not Done', 'DR Not Done'),('DR Not Required','DR Not Required')], 'DR Done')
    dr_status = fields.Selection([('Accepted', 'Accepted'), ('Rejected', 'Rejected')], 'DR Status')
    dr_remark = fields.Char('DR Number')
    dr_date = fields.Char('DR Date')
    cross_sell=fields.Selection([('No','No'),('Yes','Yes')],'Cross Sell',default='No')
    vendor_dr_id=fields.Many2one('res.partner',string='Billing from',required=True)
class deal_type_info(models.Model):
    _name="deal_type.info"
    _rec_name="deal_type"
    deal_type = fields.Char(string='Deal Type')
class upload_type_info(models.Model):
    _name="upload_type.info"
    _rec_name="upload_type"
    upload_type=fields.Char("Upload Type")
    
class upload_tab_info(models.Model):
    _name="upload_tab.info"
    order_upload_id=fields.Many2one("sale.order",string='Order Upload Reference', ondelete='cascade', index=True, copy=False)
    type=fields.Many2one("upload_type.info",string="Upload Type")
    upload_file=fields.Binary("Upload File")
    filename=fields.Char()
    verbal=fields.Text("Verbal Communication")
    
                    