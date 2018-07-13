from odoo import models, fields, api
from pprint import pprint

class wizard_naik_kelas(models.Model):
    _name = 'siswa_sd_ocb11.wizard_naik_kelas'

    name = fields.Char('Kenaikan Kelas')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", required=True, ondelete="cascade")
    next_tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran Kenaikan", required=True)
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required="1")
    next_jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang Kenaikan')
    siswa_ids = fields.One2many('siswa_sd_ocb11.wizard_naik_kelas_siswa_rel', inverse_name='wizard_id', string='Siswa')

    @api.onchange('jenjang_id')
    def onchange_jenjang(self):
        domain = {'next_jenjang_id':[('order','=',self.jenjang_id.order+1)]}
        return {'domain':domain, 'value':{'next_jenjang_id':[]}}

    # @api.multi 
    # def action_save(self):
    #     self.ensure_one()


        
    #     # add calon siswa
    #     calon_siswas = self.env['res.partner'].search(['&','&','&',
    #                                                 ('tahunajaran_id','=',self.tahunajaran_id.id),
    #                                                 ('jenjang_id','=',self.jenjang_id.id),
    #                                                 ('state','=','reg'),
    #                                                 ('is_distributed','=',False)
    #                                                 ])
    #     reg_cs = []
    #     for cs in calon_siswas:
    #         self.write({
    #             'calon_siswa_ids' : [(4,cs.id)]
    #         })
    #     # filter rombel
        
    #     return {
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'siswa_psb_ocb11.wizard_distribusi_siswa',
    #         'target': 'current',
    #         'res_id': self.id,
    #         # 'domain' : [('wizard_stock_on_hand_id','=',self.id)],
    #         # 'context' : {'search_default_group_location_id':1,'search_default_group_product_id':1},
    #         # 'context' : ctx,
    #         'type': 'ir.actions.act_window'
    #     }

    