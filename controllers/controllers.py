# -*- coding: utf-8 -*-
from odoo import http

# class SiswaSdOcb11(http.Controller):
#     @http.route('/siswa_sd_ocb11/siswa_sd_ocb11/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/siswa_sd_ocb11/siswa_sd_ocb11/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('siswa_sd_ocb11.listing', {
#             'root': '/siswa_sd_ocb11/siswa_sd_ocb11',
#             'objects': http.request.env['siswa_sd_ocb11.siswa_sd_ocb11'].search([]),
#         })

#     @http.route('/siswa_sd_ocb11/siswa_sd_ocb11/objects/<model("siswa_sd_ocb11.siswa_sd_ocb11"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('siswa_sd_ocb11.object', {
#             'object': obj
#         })