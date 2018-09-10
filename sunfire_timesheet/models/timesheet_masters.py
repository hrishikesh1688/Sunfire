from odoo import api,models,fields
class category_info(models.Model):
    _name="category.info"
    _rec_name="category"
    category=fields.Char("Category")
    catg_line=fields.One2many('sub_category.info','category_id')
class sub_category_info(models.Model):
    _name="sub_category.info"
    _rec_name="sub_category"
    sub_category=fields.Char("Sub Category")
    category_id=fields.Many2one('category.info',string='Category')