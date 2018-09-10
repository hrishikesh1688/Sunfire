from odoo import api, fields, models
import datetime

class sunfire_timesheet(models.Model):
    _name = 'sunfire.timesheet'
    _rec_name='timesheet_date'
    _sql_constraints = [ ('unique_date', 'unique(timesheet_date,create_uid)', 'Timesheet of the date entered already exists')	]
    name = fields.Char(string='Name')
    timesheet_date=fields.Date("Date",required=True)
    timesheet_line=fields.One2many("sunfire.timesheet.line","timesheet_id")
    total_time = fields.Float(string='Total time(minuntes)',compute='compute_time')
    total_time_hrs=fields.Char(string="Total time",compute='compute_time',readonly=True)
    @api.depends('timesheet_line.timespent')
    def compute_time(self):
        for line in self:
            if line.timesheet_line:
                for time in line.timesheet_line:
                    if time.timespent:
                        line.total_time+=time.timespent
                minute=line.total_time
                hrs=minute//60
                rem=minute%60
                total_hrs='{}Hr {}mins'.format(int(hrs),int(rem))
                line.total_time_hrs=total_hrs
                #print(line.total_time_hrs)
    # @api.model
    # def create(self):
    #     for order in self:
    #         for ids in order.timesheet_line:
    #             ids.rep_date=self.timesheet_date
    
class sunfire_timesheet_line(models.Model):
    _name="sunfire.timesheet.line"
    
    category=fields.Many2one('category.info',string="Category")
    sub_category=fields.Many2one('sub_category.info',string='Sub-category')
    customer=fields.Many2one('res.partner',string='Customer')
    timespent=fields.Integer("Time Spent")
    timesheet_id=fields.Many2one('sunfire.timesheet',string='Timesheet Date')
    remark=fields.Char(string="Remarks")
    rep_date=fields.Date(related="timesheet_id.timesheet_date")
    
    @api.onchange('category')
    def onchgcatg(self):
        catg_obj=self.env['category.info']
        subcatg_list=[]
        domain={}
        for order in self:
            if order.category:
                for ids in order.category:
                    catg_ids=catg_obj.search([('category','=',ids.category)])
                    print("catg_ids============>",catg_ids)
                    for order in catg_ids:
                        for ids in order.catg_line:
                            subcatg_list.append(ids.id)
                    domain['sub_category']=[('id','in',subcatg_list)]
        return {'domain':domain}