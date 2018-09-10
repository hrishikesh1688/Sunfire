from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from num2words import num2words
from itertools import groupby


class purchaseorderreport(models.Model):
    _inherit = "purchase.order"
    amount_total_words = fields.Char("Total (In Words)", compute="_compute_amount_total_words")
    
    @api.depends('amount_total')
    def _compute_amount_total_words(self):
        for purchase in self:
            purchase.amount_total_words = purchase.currency_id.amount_to_text(purchase.amount_total)

    # @api.multi
    # def set_amt_in_worlds(self,amount):
    #     return num2words(amount,lang='en_IN').replace(',', ' ').title()

    @api.multi
    def set_amt_in_worlds(self,amount):

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
          
        return finalamount
    @api.multi
    def purchase_lines_layouted(self):
        """
        Returns this sales order lines ordered by sale_layout_category sequence. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        print('self.order_id',self.order_line)
        
        for category, lines in groupby(self.order_line, lambda l: l.saleorder_line_id.layout_category_id):
            #print('l.saleorder_line_id.layout_category_id',l.saleorder_line_id)
            # If last added category induced a pagebreak, this one will be on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })
        print('report_pages',report_pages)
        return report_pages
