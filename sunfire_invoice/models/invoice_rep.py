from odoo import tools

from odoo import api, fields, models
from num2words import num2words


class account_invoice(models.Model):
    _inherit = "account.invoice"
    @api.multi
    def my_func(self):
        sale_order_obj=self.env["sale.order"]
        se_id=sale_order_obj.search([('name','=',self.origin)])
        return se_id.opf_name
        
    @api.multi
    def my_address(self):
        address_street=[]
        domain={}
        sale_order_obj=self.env["sale.order"]
        se_id=sale_order_obj.search([('name','=',self.origin)])
        address_street.append(se_id.partner_invoice_id.street)
        address_street.append(se_id.partner_invoice_id.street2)
        address_street.append(se_id.partner_invoice_id.city)
        address_street.append(se_id.partner_invoice_id.zip)
        address_street.append(se_id.partner_invoice_id.vat)
        address_street.append(se_id.partner_invoice_id.state_id.l10n_in_tin)
        address_street.append(se_id.partner_invoice_id.state_id.name)
        print('address_street',address_street)
        return address_street

    @api.multi
    def get_num(self,x):
        return str(x[10:14])
        # return float(''.join(ele for ele in x if ele.isdigit()))
    def get_num_igst(self,x):
        return str(x[4:8])
    @api.multi
    def set_amt_in_worlds(self,amount):
        if amount !=0:
            print('****amount**',amount)
            split_num=str(amount).split('.')

            int_part=int(split_num[0])

            decimal_part=int(split_num[1])

            print('*****int',int_part)
            print('*****decimal',decimal_part)
            print('****amount**',amount)

            

            fld=0.00
            amt=0
            flagdecima=0.00
            amt,fld=divmod(amount,1)
            flagdecima= fld*100
            print("***********************************{:.0f}".format(flagdecima))

            temp="{:.0f}".format(flagdecima)
            
            a=int(temp)
            print("****************a***********",a)
            

            amountinwordf=num2words(amt,lang='en_IN').replace(',', ' ').title()
            amountinwords=num2words(a,lang='en_IN').replace(',', ' ').title()

            #print('****amount**',amount)

            # print('******fld********', fld)   
            # print('*****************', round(amt,0))   
            # print('********flagdecima*********',flagdecima) 
            # print('*****************',amountinwordf)   
            # print('*****************',amountinwords) 


            finalamount='Rupees '+amountinwordf+' and Paise '+ amountinwords +" Only"
        else :
            finalamount='Zero Only'

        return finalamount

    @api.multi
    def my_func_solid(self,productid):
        sale_order_obj=self.env["sale.order"]
        sale_order_line_obj=self.env["sale.order.line"]
        se_id=sale_order_obj.search([('name','=',self.origin)])
        print('SEID***********',se_id.id)
        print('**********Product',productid)
        sol_id=sale_order_line_obj.search([('order_id','=',se_id.id),('product_id','=',productid)])
        print('***********Serial No**********',sol_id.product_serial_no)
        return sol_id.product_serial_no
    