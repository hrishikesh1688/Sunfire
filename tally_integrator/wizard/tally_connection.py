from odoo import api, fields, models, _
import os
import requests
import time
import datetime
import json
from odoo.exceptions import UserError
from random import randrange
from odoo.http import request
import geocoder
import urllib


os.environ['http_proxy']=''
class tally_connection(models.Model):
	_name = 'tally.connection'
	_description = 'Tally Connection'
	
	# @api.multi
	# def getData(self,reportType):
	# 	headers = {"Content-type": "text/xml"}
	# 	params = """<ENVELOPE><HEADER>
    #             <TALLYREQUEST>Export Data</TALLYREQUEST></HEADER>
    #             <BODY><EXPORTDATA><REQUESTDESC>
    #             <SVEXPORTFORMAT>Windows:XML</SVEXPORTFORMAT> 
    #             <ACCOUNTTYPE>""" + reportType + """</ACCOUNTTYPE>
    #             <REPORTNAME>List of Accounts</REPORTNAME></REQUESTDESC>
    #             </EXPORTDATA></BODY>
    #             </ENVELOPE>"""
	# 	try:
	# 		outstr=''
	# 		#print('Connection 2 -------',url)			
	# 		r = requests.get(url, data=params,headers=headers)
	# 		outstr = r.content
	# 		f = open('/home/sai14/Documents/temp.xml','w')
	# 		f.write(outstr.decode('utf-8'))
	# 		f.close()
	# 		raise UserError(_('suuccessfully'))
	# 		#print('Success---------',f)
	# 	except Exception as e:
	# 		raise UserError(_(str(e)))
	# 	return r

    # def send_tally(self,  context=None):
    #     ledgers = "Ledgers"
    #     if ledgers:
    #         s = self.sendData()								
    #     return {}   
    # def tally_main(self,  context=None):
    #     print('--------------',url)
    #     ledgers = "Ledgers"		
    #     if ledgers:
    #         s = self.getData("Ledgers")							
    #     return {}   
   

class account_invoice_sendtotally(models.Model):
    _inherit = "account.invoice"
    _description = "account invoice send to tally"

    # create_by | create_date | update_by | update_date
    # Ganesh      30/06/2018                
    # Info : This function use to send the invoice data in TallyERP9
    @api.multi
    def send_tally(self):        
        account_invoice_data_obj = self.env['account.invoice']
        sale_order_data_obj=self.env['sale.order']
        purchase_order_data_obj=self.env['purchase.order']
        account_invoice_line_obj = self.env['account.invoice.line']
        account_invoice_tax_obj = self.env['account.invoice.tax']

        aidata = account_invoice_data_obj.search([('number','=',self.number)])
        #print('-------id',aidata.id)
        sale_order =sale_order_data_obj.search([('name','=',aidata.origin)])      
        ail_data =account_invoice_line_obj.search([('invoice_id','=',aidata.id)])
        po_data = purchase_order_data_obj.search([('origin','=',sale_order.opf_name)])

        datestr=datetime.datetime.strptime(aidata.date_invoice, "%Y-%m-%d")
        invociedate = datestr.strftime("%d-%b-%Y at %H:%M")
        dateinvoice = datestr.strftime("%Y%m%d")
        #print('---------dsd',invociedate)
        alterid = randrange(0, 100000)
        print('---------alterid',alterid)
        masterid = randrange(0, 100000)
        print('---------masterid',masterid)
        
        itemDtl=''
        headers = {"Content-type": "text/xml"}
        itemtaxdtl=''
        for record in ail_data:
            itemDtl +="""<ALLINVENTORYENTRIES.LIST>
            <BASICUSERDESCRIPTION.LIST TYPE="String">
            <BASICUSERDESCRIPTION>"""+format(record.name.replace('&','&amp;'))+"""</BASICUSERDESCRIPTION>
            </BASICUSERDESCRIPTION.LIST>
            <STOCKITEMNAME>Annual Maintenance services</STOCKITEMNAME>
            <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
            <ISLASTDEEMEDPOSITIVE>No</ISLASTDEEMEDPOSITIVE>
            <ISAUTONEGATE>No</ISAUTONEGATE>
            <ISCUSTOMSCLEARANCE>No</ISCUSTOMSCLEARANCE>
            <ISTRACKCOMPONENT>No</ISTRACKCOMPONENT>
            <ISTRACKPRODUCTION>No</ISTRACKPRODUCTION>
            <ISPRIMARYITEM>No</ISPRIMARYITEM>
            <ISSCRAP>No</ISSCRAP>
            <RATE>"""+format(record.price_subtotal)+"""/NO.</RATE>
            <AMOUNT>"""+format(record.price_subtotal)+"""</AMOUNT>
            <ACTUALQTY>"""+format(record.quantity)+""" NO.</ACTUALQTY>
            <BILLEDQTY>"""+format(record.quantity )+""" NO.</BILLEDQTY>
            <BATCHALLOCATIONS.LIST>
            <GODOWNNAME>Stock &amp; Service</GODOWNNAME>
            <BATCHNAME>Primary Batch</BATCHNAME>
            <DESTINATIONGODOWNNAME>Stock &amp; Service</DESTINATIONGODOWNNAME>
            <INDENTNO/>
            <ORDERNO/>
            <TRACKINGNUMBER/>
            <DYNAMICCSTISCLEARED>No</DYNAMICCSTISCLEARED>
            <AMOUNT>"""+format(record.price_subtotal)+"""</AMOUNT>
            <ACTUALQTY>"""+format(round(record.quantity,0))+""" NO.</ACTUALQTY>
            <BILLEDQTY>"""+format(round(record.quantity,0))+""" NO.</BILLEDQTY>
            <ADDITIONALDETAILS.LIST>        </ADDITIONALDETAILS.LIST>
            <VOUCHERCOMPONENTLIST.LIST>        </VOUCHERCOMPONENTLIST.LIST>
            </BATCHALLOCATIONS.LIST>
            <ACCOUNTINGALLOCATIONS.LIST>
            <OLDAUDITENTRYIDS.LIST TYPE="Number">
            <OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS>
            </OLDAUDITENTRYIDS.LIST>            
            <LEDGERNAME>"""+format(record.invoice_line_tax_ids.name)+"""</LEDGERNAME>
            <GSTCLASS/>
            <GSTOVRDNNATURE>Sales Taxable</GSTOVRDNNATURE>
            <GSTOVRDNTAXABILITY>Taxable</GSTOVRDNTAXABILITY>
            <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
            <LEDGERFROMITEM>No</LEDGERFROMITEM>
            <REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>
            <ISPARTYLEDGER>No</ISPARTYLEDGER>
            <ISLASTDEEMEDPOSITIVE>No</ISLASTDEEMEDPOSITIVE>
            <ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED>
            <ISCAPVATNOTCLAIMED>No</ISCAPVATNOTCLAIMED>
            <AMOUNT>"""+format(record.price_subtotal)+"""</AMOUNT>
			<GSTOVRDNASSESSABLEVALUE>"""+format(record.price_subtotal)+"""</GSTOVRDNASSESSABLEVALUE>
			<SERVICETAXDETAILS.LIST>        </SERVICETAXDETAILS.LIST>
			<BANKALLOCATIONS.LIST>        </BANKALLOCATIONS.LIST>
			<BILLALLOCATIONS.LIST>        </BILLALLOCATIONS.LIST>
			<INTERESTCOLLECTION.LIST>        </INTERESTCOLLECTION.LIST>
			<OLDAUDITENTRIES.LIST>        </OLDAUDITENTRIES.LIST>
			<ACCOUNTAUDITENTRIES.LIST>        </ACCOUNTAUDITENTRIES.LIST>
			<AUDITENTRIES.LIST>        </AUDITENTRIES.LIST>
			<INPUTCRALLOCS.LIST>        </INPUTCRALLOCS.LIST>
			<DUTYHEADDETAILS.LIST>        </DUTYHEADDETAILS.LIST>
			<EXCISEDUTYHEADDETAILS.LIST>        </EXCISEDUTYHEADDETAILS.LIST>
			<RATEDETAILS.LIST>
			<GSTRATEDUTYHEAD>Integrated Tax</GSTRATEDUTYHEAD>
			<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
			</RATEDETAILS.LIST>
			<RATEDETAILS.LIST>
			<GSTRATEDUTYHEAD>Central Tax</GSTRATEDUTYHEAD>
			<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
			</RATEDETAILS.LIST>
			<RATEDETAILS.LIST>
			<GSTRATEDUTYHEAD>State Tax</GSTRATEDUTYHEAD>
			<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
			</RATEDETAILS.LIST>
			<RATEDETAILS.LIST>
			<GSTRATEDUTYHEAD>Cess</GSTRATEDUTYHEAD>
			<GSTRATEVALUATIONTYPE>Based on Value</GSTRATEVALUATIONTYPE>
			</RATEDETAILS.LIST>
			<SUMMARYALLOCS.LIST>        </SUMMARYALLOCS.LIST>
			<STPYMTDETAILS.LIST>        </STPYMTDETAILS.LIST>
			<EXCISEPAYMENTALLOCATIONS.LIST>        </EXCISEPAYMENTALLOCATIONS.LIST>
			<TAXBILLALLOCATIONS.LIST>        </TAXBILLALLOCATIONS.LIST>
			<TAXOBJECTALLOCATIONS.LIST>        </TAXOBJECTALLOCATIONS.LIST>
			<TDSEXPENSEALLOCATIONS.LIST>        </TDSEXPENSEALLOCATIONS.LIST>
			<VATSTATUTORYDETAILS.LIST>        </VATSTATUTORYDETAILS.LIST>
			<COSTTRACKALLOCATIONS.LIST>        </COSTTRACKALLOCATIONS.LIST>
			<REFVOUCHERDETAILS.LIST>        </REFVOUCHERDETAILS.LIST>
			<INVOICEWISEDETAILS.LIST>        </INVOICEWISEDETAILS.LIST>
			<VATITCDETAILS.LIST>        </VATITCDETAILS.LIST>
			<ADVANCETAXDETAILS.LIST>        </ADVANCETAXDETAILS.LIST>
			</ACCOUNTINGALLOCATIONS.LIST>
			<DUTYHEADDETAILS.LIST>       </DUTYHEADDETAILS.LIST>
			<SUPPLEMENTARYDUTYHEADDETAILS.LIST>       </SUPPLEMENTARYDUTYHEADDETAILS.LIST>
			<TAXOBJECTALLOCATIONS.LIST>       </TAXOBJECTALLOCATIONS.LIST>
			<REFVOUCHERDETAILS.LIST>       </REFVOUCHERDETAILS.LIST>
			<EXCISEALLOCATIONS.LIST>       </EXCISEALLOCATIONS.LIST>
			<EXPENSEALLOCATIONS.LIST>       </EXPENSEALLOCATIONS.LIST>
			</ALLINVENTORYENTRIES.LIST>"""

            self._cr.execute("select at.id,ailt.tax_id,ailt.invoice_line_id,at.name,round(at.amount,0) as rate,round(((ail.price_subtotal*at.amount)/100),2) as tax_amt  from account_invoice_line_tax ailt inner join account_invoice_line ail on ail.id=ailt.invoice_line_id inner join account_tax_filiation_rel atfr on atfr.parent_tax = ailt.tax_id and ailt.invoice_line_id = %s inner join account_tax at on at.id=atfr.child_tax",(record.id,))
            for res in self.env.cr.fetchall():
                # print('AIL tax data child tax-------',res[0])
                # print('AIL tax data parent tax-------',res[1])
                # print('AIL tax data name-------',res[3])
                # print('AIL tax data rate-------',res[4])
                itemtaxdtl+="""<LEDGERENTRIES.LIST>
                <OLDAUDITENTRYIDS.LIST TYPE="Number">
                <OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS>
                </OLDAUDITENTRYIDS.LIST>
                <BASICRATEOFINVOICETAX.LIST TYPE="Number">
                <BASICRATEOFINVOICETAX> """+format(res[4])+"""</BASICRATEOFINVOICETAX>
                </BASICRATEOFINVOICETAX.LIST>
                <ROUNDTYPE>Normal Rounding</ROUNDTYPE>
                <LEDGERNAME>"""+format(res[3])+"""</LEDGERNAME>
                <GSTCLASS/>
                <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                <LEDGERFROMITEM>No</LEDGERFROMITEM>
                <REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>
                <ISPARTYLEDGER>No</ISPARTYLEDGER>
                <ISLASTDEEMEDPOSITIVE>No</ISLASTDEEMEDPOSITIVE>
                <ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED>
                <ISCAPVATNOTCLAIMED>No</ISCAPVATNOTCLAIMED>
                <ROUNDLIMIT> 0</ROUNDLIMIT>
                <AMOUNT>"""+format(res[5])+"""</AMOUNT>
                <VATEXPAMOUNT>"""+format(res[5])+"""</VATEXPAMOUNT>
                <SERVICETAXDETAILS.LIST>       </SERVICETAXDETAILS.LIST>
                <BANKALLOCATIONS.LIST>       </BANKALLOCATIONS.LIST>
                <BILLALLOCATIONS.LIST>       </BILLALLOCATIONS.LIST>
                <INTERESTCOLLECTION.LIST>       </INTERESTCOLLECTION.LIST>
                <OLDAUDITENTRIES.LIST>       </OLDAUDITENTRIES.LIST>
                <ACCOUNTAUDITENTRIES.LIST>       </ACCOUNTAUDITENTRIES.LIST>
                <AUDITENTRIES.LIST>       </AUDITENTRIES.LIST>
                <INPUTCRALLOCS.LIST>       </INPUTCRALLOCS.LIST>
                <DUTYHEADDETAILS.LIST>       </DUTYHEADDETAILS.LIST>
                <EXCISEDUTYHEADDETAILS.LIST>       </EXCISEDUTYHEADDETAILS.LIST>
                <RATEDETAILS.LIST>       </RATEDETAILS.LIST>
                <SUMMARYALLOCS.LIST>       </SUMMARYALLOCS.LIST>
                <STPYMTDETAILS.LIST>       </STPYMTDETAILS.LIST>
                <EXCISEPAYMENTALLOCATIONS.LIST>       </EXCISEPAYMENTALLOCATIONS.LIST>
                <TAXBILLALLOCATIONS.LIST>       </TAXBILLALLOCATIONS.LIST>
                <TAXOBJECTALLOCATIONS.LIST>       </TAXOBJECTALLOCATIONS.LIST>
                <TDSEXPENSEALLOCATIONS.LIST>       </TDSEXPENSEALLOCATIONS.LIST>
                <VATSTATUTORYDETAILS.LIST>       </VATSTATUTORYDETAILS.LIST>
                <COSTTRACKALLOCATIONS.LIST>       </COSTTRACKALLOCATIONS.LIST>
                <REFVOUCHERDETAILS.LIST>       </REFVOUCHERDETAILS.LIST>
                <INVOICEWISEDETAILS.LIST>       </INVOICEWISEDETAILS.LIST>
                <VATITCDETAILS.LIST>       </VATITCDETAILS.LIST>
                <ADVANCETAXDETAILS.LIST>       </ADVANCETAXDETAILS.LIST>
                </LEDGERENTRIES.LIST>
                """	

        itemhdrdata=''
        itemhdrdata="""<ENVELOPE>
            <HEADER>
            <TALLYREQUEST>Import Data</TALLYREQUEST>
            </HEADER>
            <BODY>
            <IMPORTDATA>
            <REQUESTDESC>
            <REPORTNAME>Vouchers</REPORTNAME>
            <STATICVARIABLES>
            <SVCURRENTCOMPANY>"""+format(aidata.company_id.name)+"""</SVCURRENTCOMPANY>
            </STATICVARIABLES>
            </REQUESTDESC>
            <REQUESTDATA>
            <TALLYMESSAGE xmlns:UDF="TallyUDF">
            <VOUCHER REMOTEID= "1-"""+format(aidata.number)+"""" VCHKEY="" VCHTYPE="Sales" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <ADDRESS.LIST TYPE="String">
            <ADDRESS>"""+format(aidata.partner_id.street.replace('&','&amp;'))+"""</ADDRESS>
            <ADDRESS>"""+format(aidata.partner_id.street2.replace('&','&amp;'))+"""</ADDRESS>
            <ADDRESS>"""+format(aidata.partner_id.state_id.name)+"""</ADDRESS>
            <ADDRESS>"""+format(aidata.partner_id.state_id.name)+"""-"""+format(aidata.partner_id.zip)+""", """+format(aidata.partner_id.country_id.name)+"""</ADDRESS>
            </ADDRESS.LIST>
            <BASICBUYERADDRESS.LIST TYPE="String">
            <BASICBUYERADDRESS>"""+format(aidata.partner_id.street.replace('&','&amp;'))+"""</BASICBUYERADDRESS>
            <BASICBUYERADDRESS>"""+format(aidata.partner_id.street2.replace('&','&amp;'))+"""</BASICBUYERADDRESS>
            <BASICBUYERADDRESS>"""+format(aidata.partner_id.state_id.name)+"""</BASICBUYERADDRESS>
            <BASICBUYERADDRESS>"""+format(aidata.partner_id.state_id.name)+"""-"""+format(aidata.partner_id.zip)+""", """+format(aidata.partner_id.country_id.name)+"""</BASICBUYERADDRESS>
            </BASICBUYERADDRESS.LIST>
            <OLDAUDITENTRYIDS.LIST TYPE="Number">
            <OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS>
            </OLDAUDITENTRYIDS.LIST>
            <DATE>"""+format(dateinvoice)+"""</DATE>
            <GUID>1-"""+format(aidata.number)+"""</GUID>
            <STATENAME>"""+format(aidata.partner_id.state_id.name)+"""</STATENAME>
            <GSTREGISTRATIONTYPE>Regular</GSTREGISTRATIONTYPE>
            <VATDEALERTYPE>Regular</VATDEALERTYPE>
            <COUNTRYOFRESIDENCE>"""+format(aidata.partner_id.country_id.name)+"""</COUNTRYOFRESIDENCE>
            <PARTYGSTIN>"""+format(aidata.partner_id.vat)+"""</PARTYGSTIN>
            <PARTYNAME>"""+format(aidata.partner_id.name)+"""</PARTYNAME>
            <VOUCHERTYPENAME>Sales</VOUCHERTYPENAME>
            <REFERENCE>"""+format(sale_order.opf_name)+"""</REFERENCE>
            <VOUCHERNUMBER>"""+format(aidata.number)+"""</VOUCHERNUMBER>
            <PARTYLEDGERNAME>"""+format(aidata.partner_id.name)+"""</PARTYLEDGERNAME>
            <BASICBASEPARTYNAME>"""+format(aidata.partner_id.name)+"""</BASICBASEPARTYNAME>
            <CSTFORMISSUETYPE/>
            <CSTFORMRECVTYPE/>
            <CONSIGNEECSTNUMBER> </CONSIGNEECSTNUMBER>
            <BUYERSCSTNUMBER> </BUYERSCSTNUMBER>
            <FBTPAYMENTTYPE>Default</FBTPAYMENTTYPE>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>
            <PLACEOFSUPPLY>"""+format(sale_order.partner_shipping_id.state_id.name)+"""</PLACEOFSUPPLY>
            <CONSIGNEEGSTIN>"""+format(aidata.partner_id.vat)+"""</CONSIGNEEGSTIN>
            <BASICBUYERNAME>"""+format(aidata.partner_id.name)+"""</BASICBUYERNAME>
            <BASICDUEDATEOFPYMT>"""+format(sale_order.payment_term_id.name)+"""</BASICDUEDATEOFPYMT>
            <BASICDATETIMEOFINVOICE>"""+format(invociedate)+"""</BASICDATETIMEOFINVOICE>
            <BASICDATETIMEOFREMOVAL>"""+format(invociedate)+"""</BASICDATETIMEOFREMOVAL>
            <VCHGSTCLASS/>
            <CONSIGNEESTATENAME>"""+format(aidata.partner_id.state_id.name)+"""</CONSIGNEESTATENAME>
            <ENTEREDBY>admin</ENTEREDBY>
            <DIFFACTUALQTY>No</DIFFACTUALQTY>
            <ISMSTFROMSYNC>No</ISMSTFROMSYNC>
            <ASORIGINAL>No</ASORIGINAL>
            <AUDITED>No</AUDITED>
            <FORJOBCOSTING>No</FORJOBCOSTING>
            <ISOPTIONAL>No</ISOPTIONAL>
            <EFFECTIVEDATE>"""+format(dateinvoice)+"""</EFFECTIVEDATE>
            <USEFOREXCISE>No</USEFOREXCISE>
            <ISFORJOBWORKIN>No</ISFORJOBWORKIN>
            <ALLOWCONSUMPTION>No</ALLOWCONSUMPTION>
            <USEFORINTEREST>No</USEFORINTEREST>
            <USEFORGAINLOSS>No</USEFORGAINLOSS>
            <USEFORGODOWNTRANSFER>No</USEFORGODOWNTRANSFER>
            <USEFORCOMPOUND>No</USEFORCOMPOUND>
            <USEFORSERVICETAX>No</USEFORSERVICETAX>
            <ISEXCISEVOUCHER>No</ISEXCISEVOUCHER>
            <EXCISETAXOVERRIDE>No</EXCISETAXOVERRIDE>
            <USEFORTAXUNITTRANSFER>No</USEFORTAXUNITTRANSFER>
            <EXCISEOPENING>No</EXCISEOPENING>
            <USEFORFINALPRODUCTION>No</USEFORFINALPRODUCTION>
            <ISTDSOVERRIDDEN>No</ISTDSOVERRIDDEN>
            <ISTCSOVERRIDDEN>No</ISTCSOVERRIDDEN>
            <ISTDSTCSCASHVCH>No</ISTDSTCSCASHVCH>
            <INCLUDEADVPYMTVCH>No</INCLUDEADVPYMTVCH>
            <ISSUBWORKSCONTRACT>No</ISSUBWORKSCONTRACT>
            <ISVATOVERRIDDEN>No</ISVATOVERRIDDEN>
            <IGNOREORIGVCHDATE>No</IGNOREORIGVCHDATE>
            <ISVATPAIDATCUSTOMS>No</ISVATPAIDATCUSTOMS>
            <ISDECLAREDTOCUSTOMS>No</ISDECLAREDTOCUSTOMS>
            <ISSERVICETAXOVERRIDDEN>No</ISSERVICETAXOVERRIDDEN>
            <ISISDVOUCHER>No</ISISDVOUCHER>
            <ISEXCISEOVERRIDDEN>No</ISEXCISEOVERRIDDEN>
            <ISEXCISESUPPLYVCH>No</ISEXCISESUPPLYVCH>
            <ISGSTOVERRIDDEN>No</ISGSTOVERRIDDEN>
            <GSTNOTEXPORTED>No</GSTNOTEXPORTED>
            <ISVATPRINCIPALACCOUNT>No</ISVATPRINCIPALACCOUNT>
            <ISBOENOTAPPLICABLE>No</ISBOENOTAPPLICABLE>
            <ISSHIPPINGWITHINSTATE>No</ISSHIPPINGWITHINSTATE>
            <ISOVERSEASTOURISTTRANS>No</ISOVERSEASTOURISTTRANS>
            <ISDESIGNATEDZONEPARTY>No</ISDESIGNATEDZONEPARTY>
            <ISCANCELLED>No</ISCANCELLED>
            <HASCASHFLOW>No</HASCASHFLOW>
            <ISPOSTDATED>No</ISPOSTDATED>
            <USETRACKINGNUMBER>No</USETRACKINGNUMBER>
            <ISINVOICE>Yes</ISINVOICE>
            <MFGJOURNAL>No</MFGJOURNAL>
            <HASDISCOUNTS>No</HASDISCOUNTS>
            <ASPAYSLIP>No</ASPAYSLIP>
            <ISCOSTCENTRE>No</ISCOSTCENTRE>
            <ISSTXNONREALIZEDVCH>No</ISSTXNONREALIZEDVCH>
            <ISEXCISEMANUFACTURERON>No</ISEXCISEMANUFACTURERON>
            <ISBLANKCHEQUE>No</ISBLANKCHEQUE>
            <ISVOID>No</ISVOID>
            <ISONHOLD>No</ISONHOLD>
            <ORDERLINESTATUS>No</ORDERLINESTATUS>
            <VATISAGNSTCANCSALES>No</VATISAGNSTCANCSALES>
            <VATISPURCEXEMPTED>No</VATISPURCEXEMPTED>
            <ISVATRESTAXINVOICE>No</ISVATRESTAXINVOICE>
            <VATISASSESABLECALCVCH>No</VATISASSESABLECALCVCH>
            <ISVATDUTYPAID>Yes</ISVATDUTYPAID>
            <ISDELIVERYSAMEASCONSIGNEE>No</ISDELIVERYSAMEASCONSIGNEE>
            <ISDISPATCHSAMEASCONSIGNOR>No</ISDISPATCHSAMEASCONSIGNOR>
            <ISDELETED>No</ISDELETED>
            <CHANGEVCHMODE>No</CHANGEVCHMODE>
            <ALTERID> """+format(alterid)+"""</ALTERID>
            <MASTERID> """+format(masterid)+"""</MASTERID>
            <VOUCHERKEY></VOUCHERKEY>
            <EXCLUDEDTAXATIONS.LIST>      </EXCLUDEDTAXATIONS.LIST>
            <OLDAUDITENTRIES.LIST>      </OLDAUDITENTRIES.LIST>
            <ACCOUNTAUDITENTRIES.LIST>      </ACCOUNTAUDITENTRIES.LIST>
            <AUDITENTRIES.LIST>      </AUDITENTRIES.LIST>
            <DUTYHEADDETAILS.LIST>      </DUTYHEADDETAILS.LIST>
            <SUPPLEMENTARYDUTYHEADDETAILS.LIST>      </SUPPLEMENTARYDUTYHEADDETAILS.LIST>
            <EWAYBILLDETAILS.LIST>      </EWAYBILLDETAILS.LIST>
            <INVOICEDELNOTES.LIST>
            <BASICSHIPPINGDATE>"""+format(dateinvoice)+"""</BASICSHIPPINGDATE>
            <BASICSHIPDELIVERYNOTE>"""+format(aidata.number)+"""</BASICSHIPDELIVERYNOTE>
            </INVOICEDELNOTES.LIST>
            <INVOICEORDERLIST.LIST>
            <BASICORDERDATE>"""+format(dateinvoice)+"""</BASICORDERDATE>
            <BASICPURCHASEORDERNO>"""+format(aidata.name)+"""</BASICPURCHASEORDERNO>
            </INVOICEORDERLIST.LIST>
            <INVOICEINDENTLIST.LIST>      </INVOICEINDENTLIST.LIST>
            <ATTENDANCEENTRIES.LIST>      </ATTENDANCEENTRIES.LIST>
            <ORIGINVOICEDETAILS.LIST>      </ORIGINVOICEDETAILS.LIST>
            <INVOICEEXPORTLIST.LIST>      </INVOICEEXPORTLIST.LIST>
            <LEDGERENTRIES.LIST>
            <OLDAUDITENTRYIDS.LIST TYPE="Number">
            <OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS>
            </OLDAUDITENTRYIDS.LIST>
            <LEDGERNAME>"""+format(aidata.partner_id.name)+"""</LEDGERNAME>
            <GSTCLASS/>
            <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
            <LEDGERFROMITEM>No</LEDGERFROMITEM>
            <REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>
            <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
            <ISLASTDEEMEDPOSITIVE>Yes</ISLASTDEEMEDPOSITIVE>
            <ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED>
            <ISCAPVATNOTCLAIMED>No</ISCAPVATNOTCLAIMED>
            <AMOUNT>-"""+format(aidata.amount_total)+"""</AMOUNT>
            <SERVICETAXDETAILS.LIST></SERVICETAXDETAILS.LIST>
            <BANKALLOCATIONS.LIST></BANKALLOCATIONS.LIST>
            <BILLALLOCATIONS.LIST>
            <NAME>"""+format(aidata.number)+"""</NAME>
            <BILLTYPE>New Ref</BILLTYPE>
            <TDSDEDUCTEEISSPECIALRATE>No</TDSDEDUCTEEISSPECIALRATE>
			<AMOUNT>-"""+format(aidata.amount_total)+"""</AMOUNT>
            <INTERESTCOLLECTION.LIST></INTERESTCOLLECTION.LIST>
            <STBILLCATEGORIES.LIST>        </STBILLCATEGORIES.LIST>
            </BILLALLOCATIONS.LIST>
            <INTERESTCOLLECTION.LIST></INTERESTCOLLECTION.LIST>
            <OLDAUDITENTRIES.LIST></OLDAUDITENTRIES.LIST>
            <ACCOUNTAUDITENTRIES.LIST></ACCOUNTAUDITENTRIES.LIST>
            <AUDITENTRIES.LIST>       </AUDITENTRIES.LIST>
            <INPUTCRALLOCS.LIST>       </INPUTCRALLOCS.LIST>
            <DUTYHEADDETAILS.LIST>       </DUTYHEADDETAILS.LIST>
            <EXCISEDUTYHEADDETAILS.LIST>       </EXCISEDUTYHEADDETAILS.LIST>
            <RATEDETAILS.LIST>       </RATEDETAILS.LIST>
            <SUMMARYALLOCS.LIST>       </SUMMARYALLOCS.LIST>
            <STPYMTDETAILS.LIST>       </STPYMTDETAILS.LIST>
            <EXCISEPAYMENTALLOCATIONS.LIST>       </EXCISEPAYMENTALLOCATIONS.LIST>
            <TAXBILLALLOCATIONS.LIST>       </TAXBILLALLOCATIONS.LIST>
            <TAXOBJECTALLOCATIONS.LIST>       </TAXOBJECTALLOCATIONS.LIST>
            <TDSEXPENSEALLOCATIONS.LIST>       </TDSEXPENSEALLOCATIONS.LIST>
            <VATSTATUTORYDETAILS.LIST>       </VATSTATUTORYDETAILS.LIST>
            <COSTTRACKALLOCATIONS.LIST>       </COSTTRACKALLOCATIONS.LIST>
            <REFVOUCHERDETAILS.LIST>       </REFVOUCHERDETAILS.LIST>
            <INVOICEWISEDETAILS.LIST>       </INVOICEWISEDETAILS.LIST>
            <VATITCDETAILS.LIST>       </VATITCDETAILS.LIST>
            <ADVANCETAXDETAILS.LIST>       </ADVANCETAXDETAILS.LIST>
            </LEDGERENTRIES.LIST>
            <LEDGERENTRIES.LIST>
            <OLDAUDITENTRYIDS.LIST TYPE="Number">
            <OLDAUDITENTRYIDS>-1</OLDAUDITENTRYIDS>
            </OLDAUDITENTRYIDS.LIST>
            <LEDGERNAME>GST Net Sale</LEDGERNAME>
            <GSTCLASS/>
            <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
            <LEDGERFROMITEM>No</LEDGERFROMITEM>
            <REMOVEZEROENTRIES>No</REMOVEZEROENTRIES>
            <ISPARTYLEDGER>No</ISPARTYLEDGER>
            <ISLASTDEEMEDPOSITIVE>No</ISLASTDEEMEDPOSITIVE>
            <ISCAPVATTAXALTERED>No</ISCAPVATTAXALTERED>
            <AMOUNT>"""+format(aidata.amount_untaxed)+"""</AMOUNT>
            <SERVICETAXDETAILS.LIST>       </SERVICETAXDETAILS.LIST>
            <BANKALLOCATIONS.LIST>       </BANKALLOCATIONS.LIST>
            <BILLALLOCATIONS.LIST>       </BILLALLOCATIONS.LIST>
            <INTERESTCOLLECTION.LIST>       </INTERESTCOLLECTION.LIST>
            <OLDAUDITENTRIES.LIST>       </OLDAUDITENTRIES.LIST>
            <ACCOUNTAUDITENTRIES.LIST>       </ACCOUNTAUDITENTRIES.LIST>
            <AUDITENTRIES.LIST>       </AUDITENTRIES.LIST>
            <INPUTCRALLOCS.LIST>       </INPUTCRALLOCS.LIST>
            <DUTYHEADDETAILS.LIST>       </DUTYHEADDETAILS.LIST>
            <EXCISEDUTYHEADDETAILS.LIST>       </EXCISEDUTYHEADDETAILS.LIST>
            <RATEDETAILS.LIST>       </RATEDETAILS.LIST>
            <SUMMARYALLOCS.LIST>       </SUMMARYALLOCS.LIST>
            <STPYMTDETAILS.LIST>       </STPYMTDETAILS.LIST>
            <EXCISEPAYMENTALLOCATIONS.LIST>       </EXCISEPAYMENTALLOCATIONS.LIST>
            <TAXBILLALLOCATIONS.LIST>       </TAXBILLALLOCATIONS.LIST>
            <TAXOBJECTALLOCATIONS.LIST>       </TAXOBJECTALLOCATIONS.LIST>
            <TDSEXPENSEALLOCATIONS.LIST>       </TDSEXPENSEALLOCATIONS.LIST>
            <VATSTATUTORYDETAILS.LIST>       </VATSTATUTORYDETAILS.LIST>
            <COSTTRACKALLOCATIONS.LIST>       </COSTTRACKALLOCATIONS.LIST>
            <REFVOUCHERDETAILS.LIST>       </REFVOUCHERDETAILS.LIST>
            <INVOICEWISEDETAILS.LIST>       </INVOICEWISEDETAILS.LIST>
            <VATITCDETAILS.LIST>       </VATITCDETAILS.LIST>
            <ADVANCETAXDETAILS.LIST>       </ADVANCETAXDETAILS.LIST>
            </LEDGERENTRIES.LIST>"""+itemtaxdtl+"""<PAYROLLMODEOFPAYMENT.LIST>
            </PAYROLLMODEOFPAYMENT.LIST>
            <ATTDRECORDS.LIST>      </ATTDRECORDS.LIST>
            <GSTEWAYCONSIGNORADDRESS.LIST>      </GSTEWAYCONSIGNORADDRESS.LIST>
            <GSTEWAYCONSIGNEEADDRESS.LIST>      </GSTEWAYCONSIGNEEADDRESS.LIST>
            <TEMPGSTRATEDETAILS.LIST>      </TEMPGSTRATEDETAILS.LIST>
            </VOUCHER>
            </TALLYMESSAGE>
            <TALLYMESSAGE xmlns:UDF="TallyUDF"><COMPANY>
            <REMOTECMPINFO.LIST MERGE="Yes">
            <NAME>33924d0e-62d5-4228-bc76-595e6a82a9c2</NAME>
            <REMOTECMPNAME>"""+format(aidata.company_id.name)+"""</REMOTECMPNAME>
            <REMOTECMPSTATE>"""+format(aidata.company_id.state_id.name)+"""</REMOTECMPSTATE>
            </REMOTECMPINFO.LIST>
            </COMPANY>
            </TALLYMESSAGE>
            <TALLYMESSAGE xmlns:UDF="TallyUDF">
            <COMPANY><REMOTECMPINFO.LIST MERGE="Yes">
            <NAME>33924d0e-62d5-4228-bc76-595e6a82a9c2</NAME>
            <REMOTECMPNAME>"""+format(aidata.company_id.name)+"""</REMOTECMPNAME>
            <REMOTECMPSTATE>"""+format(aidata.company_id.state_id.name)+"""</REMOTECMPSTATE>
            </REMOTECMPINFO.LIST>
            </COMPANY>
            </TALLYMESSAGE>
            </REQUESTDATA>
            </IMPORTDATA>
            </BODY>
            </ENVELOPE>"""

        print('---data---',itemhdrdata)

        # g = geocoder.ip('180.92.175.221')
        # print('--------------latlong-----',g.latlng)        
        # Find user location        
        # with urllib.request.urlopen('http://ip-api.com/json/') as url:
        #     http_info = url.info()
        #     raw_data = url.read().decode(http_info.get_content_charset())
        #     project_info = json.loads(raw_data)
        #     result = project_info
        #     name = result['city']        
        # print('-----------data--------',name)
        
        try:
            
            print('Connection 2 -------',url)			
            r = requests.post(url, data=itemhdrdata,headers=headers)
            print(r.content)
            raise UserError(_(r.content))
            #raise UserError(_('Send suuccessfully'))
        except Exception as e:
            raise UserError(_(str(e)))

        return r

url="http://192.168.0.13:9000"

tally_connection()

