# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint

class tahunajaran(models.Model):
    _inherit = 'siswa_ocb11.tahunajaran'

    @api.model
    def create(self, vals):
        result = super(tahunajaran, self).create(vals)

        # Generate data wizard kenaikan kelas
        ## Get jenjang
        print('----------------------------------')
        print('Generate wizard kenaikan kelas')
        print('----------------------------------')
        jenjang_ids = self.env['siswa_ocb11.jenjang'].search([('name','!=','')])
        for jenjang in jenjang_ids:
            next_jenjang_id = self.env['siswa_ocb11.jenjang'].search([('order','=',jenjang.order+1)])
            self.env['siswa_sd_ocb11.wizard_naik_kelas'].create({
                'name' : result.name + ' - ' + jenjang.name,
                'tahunajaran_id' : result.id,
                'jenjang_id' : jenjang.id,
                'next_jenjang_id' : next_jenjang_id.id
            })

        return result
