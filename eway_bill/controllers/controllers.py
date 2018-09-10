# -*- coding: utf-8 -*-
from odoo import http

# class EwayBill(http.Controller):
#     @http.route('/eway_bill/eway_bill/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eway_bill/eway_bill/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('eway_bill.listing', {
#             'root': '/eway_bill/eway_bill',
#             'objects': http.request.env['eway_bill.eway_bill'].search([]),
#         })

#     @http.route('/eway_bill/eway_bill/objects/<model("eway_bill.eway_bill"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eway_bill.object', {
#             'object': obj
#         })