# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from pprint import pprint

class tahunajaran(models.Model):
    _inherit = 'siswa_ocb11.tahunajaran'

    @api.model
    def create(self, vals):
        print('Inside Tahun ajaran on Siswa SD Module')

        result = super(tahunajaran, self).create(vals)

        # Generate data wizard kenaikan kelas
        ## Get jenjang
        print('Generate wizard kenaikan kelas')
        jenjang_ids = self.env['siswa_ocb11.jenjang'].search([('name','=','')])
        for jenjang in jenjang_ids:
            next_jenjang_id = self.env['siswa_ocb11.jenjang'].search([('order','=',jenjang.order+1)])
            self.env['siswa_sd_ocb11.wizard_naik_kelas'].create({
                'tahunajaran_id' : result.id,
                'jenjang_id' : jenjang.id,
                'next_jenjang_id' : next_jenjang_id.id
            })

        return result
