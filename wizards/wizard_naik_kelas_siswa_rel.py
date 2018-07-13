from odoo import models, fields, api
from pprint import pprint

class wizard_naik_kelas_siswa_rel(models.Model):
    _name = 'siswa_sd_ocb11.wizard_naik_kelas_siswa_rel'

    name = fields.Char('Name')
    wizard_id = fields.Many2one('siswa_sd_ocb11.wizad_naik_kelas', string="Wizard Id", required=True)
    siswa_id = fields.Many2one('res.partner', string="Siswa", required=True)
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang')
    next_jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang Kenaikan')
    rombel_id = fields.Many2one('siswa_ocb1.rombel',string='Rombel')
    next_rombel_id = fields.Many2one('siswa_ocb1.rombel',string='Rombel Kenaikan')

    