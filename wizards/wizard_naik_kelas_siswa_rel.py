from flectra import models, fields, api
from pprint import pprint

class wizard_naik_kelas_siswa_rel(models.Model):
    _name = 'siswa_sd_ocb11.wizard_naik_kelas_siswa_rel'

    name = fields.Char('Name')
    wizard_id = fields.Many2one('siswa_sd_ocb11.wizad_naik_kelas', string="Wizard Id", required=True)
    siswa_id = fields.Many2one('res.partner', string="Siswa", required=True)
    nis = fields.Char('NIS',related='siswa_id.nis')
    induk = fields.Char('No. Induk',related='siswa_id.induk')
    jenis_kelamin = fields.Selection([('laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin', related='siswa_id.jenis_kelamin')
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang')
    next_jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang Kenaikan')
    rombel_id = fields.Many2one('siswa_ocb11.rombel',string='Rombel')
    next_rombel_id = fields.Many2one('siswa_ocb11.rombel',string='Rombel Kenaikan')

    @api.onchange('jenjang_id')
    def onchange_jenjang(self):
        domain = {'next_rombel_id':[('jenjang_id','=',self.next_jenjang_id.id)]}
        return {'domain':domain, 'value':{'next_rombel_id':[]}}

     