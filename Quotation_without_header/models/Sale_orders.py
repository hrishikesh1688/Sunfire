from odoo import tools
from odoo import api, fields, models


class Sale_Report(models.Model):
    _inherit = ['sale.order','res.company']
  