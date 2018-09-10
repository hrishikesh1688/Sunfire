from odoo import tools
from odoo import api, fields, models
from itertools import groupby



class Sale_Report(models.Model):
    _inherit = 'sale.order'
    @api.multi
    def order_lines_layouted_with_product(self):
        """
        Returns this sales order lines ordered by sale_layout_category sequence. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        prodcut_cat=[[]]
        order_line_no=''
        for category, lines in groupby(self.order_line, lambda l: l.layout_category_id):
            order_line_no=list(lines)
            # If last added category induced a pagebreak, this one will be on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(order_line_no),
                'flg':order_line_no[0].product_id.categ_id.name
                #.categ_id.name
            })
        print('report_pages',report_pages)
        return report_pages