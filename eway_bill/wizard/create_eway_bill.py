from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from datetime import datetime
import urllib.request
import json
import requests
import re
import webbrowser
from werkzeug.urls import url_encode
import collections
import pprint
import os
import base64
from datetime import datetime
from odoo.tools.safe_eval import safe_eval

class Createewaybill(models.Model):
    #_inherit = "ir.actions.report"
    #update status created by,date and updated by,date in table
    _name='create.eway.bill'
   
    @api.multi
    def eway_bill_generate(self):
        account_invoice_data_obj = self.env['account.invoice']
        account_invoice_line_obj = self.env['account.invoice.line']
        print('Invoice Number',account_invoice_data_obj.number)
        temp=self.env.context['active_ids']
        print('************',temp)
        data={ }
        n_list={}
        rowarray_list={ }
        sgstamt=0
        cgstamt=0
        igstamt=0
        print('OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK',data)
        n_list=[]
        head_list=''
        head_list=({
            "version":'1.0.0618',
            "billLists":[]
        })
        print('head_list',head_list)
        total=0
        sgstRate=''
        cgstRate=''
        igstRate=''
        sgstRate1=''
        cgstRate1=''
        igstRate1=''
        total_tax_amt=0
        tax_name_str=''
        transdocdate=''
        for id in temp:
            ail_data=''
            aidata=''
            aidata = account_invoice_data_obj.search([('id','=',id)])
            print('************',aidata.number)
            opf_data =account_invoice_data_obj.search([('name','=',aidata.origin)])      
            ail_data =account_invoice_line_obj.search([('invoice_id','=',aidata.id)])
            for line in ail_data:
                    price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    tax_lines = line.invoice_line_tax_ids.compute_all(price_unit, line.invoice_id.currency_id, line.quantity, line.product_id, line.invoice_id.partner_id)['taxes']
                    print('tax_lines',tax_lines)
                    if tax_lines[0]['name'].find("SGST")==0:
                        sgstamt=sgstamt+tax_lines[0]['amount']
                        cgstamt=cgstamt+tax_lines[1]['amount']
                    if tax_lines[0]['name'].find("IGST")==0:
                        sgstamt=0
                        cgstamt=0
                        igstamt=igstamt+tax_lines[0]['amount']
            data['billLists']=[]
            datestr=datetime.strptime(aidata.date_invoice, "%Y-%m-%d")
            invociedate = datestr.strftime("%d/%m/%Y")
            if aidata.transdocdate!=False:
                datestr1=datetime.strptime(aidata.transdocdate, "%Y-%m-%d")
                transdocdate = datestr1.strftime("%d/%m/%Y")


            data['billLists'].append({
                    "userGstin": format(aidata.company_id.vat),
                    "supplyType": "O",            
                    "subSupplyType": 1,
                    "docType": "INV",
                    "docNo":  format(aidata.number),
                    "docDate": format(invociedate), #"09-07-2018",
                    "fromGstin": format(aidata.company_id.vat),
                    "fromTrdName": format(aidata.company_id.name),
                    "fromAddr1": format(aidata.company_id.street),
                    "fromAddr2": format(aidata.company_id.street2),
                    "fromPlace": format(aidata.company_id.city),
                    "fromPincode": int(aidata.company_id.zip),
                    "fromStateCode": int(aidata.company_id.state_id.l10n_in_tin),
                    "actualFromStateCode": int(aidata.company_id.state_id.l10n_in_tin),
                    "toGstin": format(aidata.partner_shipping_id.vat),
                    "toTrdName": format(aidata.partner_id.name),
                    "toAddr1": format(aidata.partner_id.street),
                    "toAddr2": format(aidata.partner_id.street2) if format(aidata.partner_id.street2)==False else '' ,
                    "toPlace": format(aidata.partner_id.city),
                    "toPincode": int(aidata.partner_id.zip),
                    "toStateCode": int(aidata.partner_id.state_id.l10n_in_tin),
                    "actualtoStateCode": int(aidata.partner_shipping_id.state_id.l10n_in_tin),
                    "totalValue": aidata.amount_untaxed,
                    "cgstValue": cgstamt,  
                    "sgstValue": sgstamt,
                    "igstValue":igstamt,
                    "cessValue": 0.0,
                    "transMode": int(aidata.transmode) ,
                    "transDistance": int(aidata.transdistance), 
                    "transporterName":format(aidata.transportername) if format(aidata.transportername)==False else '' ,
                    "transporterId": format(aidata.transporterid) if format(aidata.transporterid)==False else '' ,           
                    "transDocNo":format(aidata.transdocno) ,
                    "transDocDate": format(transdocdate) ,
                    "vehicleNo":format(aidata.vehicleno) if format(aidata.vehicleno)==False else '' ,
                    "vehicleType":format(aidata.vehicletype) if format(aidata.vehicletype)==False else '' ,
                    "totInvValue":aidata.amount_total,
                    #"mainHsnCode":0,
                    "itemList": []
                })
            sgstamt=0
            cgstamt=0
            igstamt=0
            self.ensure_one()
            tax_datas = {}
            total=0
            sgstRate=''
            cgstRate=''
            igstRate=''
            sgstRate1=0
            cgstRate1=0
            igstRate1=0
            total_tax_amt=0
            tax_name_str=''
            i=1
            for n_list in data['billLists']:
                for line in ail_data:
                    price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    tax_lines = line.invoice_line_tax_ids.compute_all(price_unit, line.invoice_id.currency_id, line.quantity, line.product_id, line.invoice_id.partner_id)['taxes']
                    print('tax_lines',tax_lines)
                    if tax_lines[0]['name'].find("SGST")==0:
                        sgstRate=tax_lines[0]['name']
                        total_tax_amt=tax_lines[0]['amount']+tax_lines[1]['amount']
                        sgstRate1=sgstRate[10:14]
                        sgstRate1=sgstRate1[:-1]
                        cgstRate=tax_lines[1]['name']
                        cgstRate1=cgstRate[10:14]
                        cgstRate1=cgstRate1[:-1]
                    if tax_lines[0]['name'].find("IGST")==0:
                        igstRate=tax_lines[0]['name']
                        igstRate1=igstRate[4:8]
                        igstRate1=igstRate1[:-1]
                        total_tax_amt=tax_lines[0]['amount']
                    n_list['itemList'].append({
                                "itemNo": i,
                                "productName": line.product_id.name,
                                "productDesc": line.product_id.description,
                                "hsnCode": int(line.product_id.l10n_in_hsn_code),
                                "quantity":float(line.quantity),
                                "qtyUnit": line.uom_id.name,
                                "taxableAmount":float(total_tax_amt),
                                "sgstRate": float(sgstRate1),
                                "cgstRate": float(cgstRate1),
                                "igstRate": float(igstRate1),
                                "cessRate": 0,
                        })
                    i=i+1
                #head_list['billLists'].append(data['billLists'])
                head_list['billLists']+=data['billLists']
                data={}
                n_list={}
            full_path = os.path.realpath(__file__)
            path, filename = os.path.split(full_path)

            save_path=path.replace('wizard','download/')
            currentMonth = datetime.now()
            file_name=''
            if len(temp)>1:
                file_name = currentMonth.strftime("%Y%m%d%H%M%S") +'.json'
            else:
                file_name=format(aidata.number.replace('/',''))
                file_name=format(file_name.replace(' ','')+'.json')
            print('###################',file_name)
            print('Print fffff',head_list)
            with open(save_path+file_name, 'w') as outfile:  
                json_data = json.dump(head_list, outfile,sort_keys=True, indent=4)

            result_file = open(save_path+file_name,'rb').read()

            #print('attach_id',result_file)
            attach_id = self.env['ewaybill.json.report'].create({
                                            'name':file_name,
                                            'report':base64.encodestring(result_file)
                        })
            print('attach_id',attach_id)
            array = '{"ip": "123.201.54.60","hostname": "60-54-201-123.static.youbroadband.in","city": "Yelachenahalli","region": "Karnataka","country": "IN","loc": "12.9020,77.5709","org": "AS18207 YOU Broadband & Cable India Ltd."}'
            data123  = json.loads(array)
            
            fruits_list = data123['city']
            
            print('city',fruits_list)
        return {
            'name': 'Eway-Bill Download',
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ewaybill.json.report',
            'res_id':attach_id.id,
            'data': None,
            'type': 'ir.actions.act_window',
            'target':'new'
        }

class WizardExcelReport(models.TransientModel):
    _name = "ewaybill.json.report"
    
    report = fields.Binary('Prepared file',filters='.json', readonly=True)
    name = fields.Char('File Name', size=32)    

