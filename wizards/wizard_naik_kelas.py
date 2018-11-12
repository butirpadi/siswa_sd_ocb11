import calendar
from flectra import models, fields, api
from pprint import pprint

class wizard_naik_kelas(models.Model):
    _name = 'siswa_sd_ocb11.wizard_naik_kelas'

    name = fields.Char('Kenaikan Kelas')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
    tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran", required=True, ondelete="cascade")
    next_tahunajaran_id = fields.Many2one('siswa_ocb11.tahunajaran', string="Tahun Ajaran Kenaikan")
    jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang', required="1")
    next_jenjang_id = fields.Many2one('siswa_ocb11.jenjang', string='Jenjang Kenaikan')
    siswa_ids = fields.One2many('siswa_sd_ocb11.wizard_naik_kelas_siswa_rel', inverse_name='wizard_id', string='Siswa')
    is_collected = fields.Boolean('is collected', default=False)


    @api.onchange('jenjang_id')
    def onchange_jenjang(self):
        domain = {'next_jenjang_id':[('order','=',self.jenjang_id.order+1)]}
        return {'domain':domain, 'value':{'next_jenjang_id':[]}}
    
    def action_confirm(self):
        self.ensure_one()
        for siswa in self.siswa_ids:
            # # insert rombel_siswa
            self.env['siswa_ocb11.rombel_siswa'].create({
                'tahunajaran_id' : self.next_tahunajaran_id.id,
                'rombel_id' : siswa.next_rombel_id.id,
                'siswa_id' : siswa.siswa_id.id
            })
            # print(siswa.siswa_id.name + ' pindah ke ' + str(siswa.next_rombel_id.id))

            # assign biaya to siswa
            # :: get tahun_ajaran_jenjang
            ta_jenjang = self.env['siswa_ocb11.tahunajaran_jenjang'].search([
                        ('tahunajaran_id', '=', self.next_tahunajaran_id.id),
                        ('jenjang_id', '=', self.next_jenjang_id.id)
                    ])

            total_biaya = 0.0
            for by in ta_jenjang.biayas:
                print ('assign ' + by.biaya_id.name + ' to ' + siswa.siswa_id.name)
                if by.biaya_id.is_bulanan:
                    for bulan_index in range(1,13):
                        harga = by.harga
                        
                        if by.is_different_by_gender:
                            if siswa.siswa_id.jenis_kelamin == 'perempuan':
                                harga = by.harga_alt

                        self.env['siswa_keu_ocb11.siswa_biaya'].create({
                            'name' : by.biaya_id.name + ' ' + calendar.month_name[bulan_index],
                            'siswa_id' : siswa.siswa_id.id,
                            'tahunajaran_id' : self.next_tahunajaran_id.id,
                            'biaya_id' : by.biaya_id.id,
                            'bulan' : bulan_index,
                            'harga' : harga,
                            'amount_due' : harga,
                            'jenjang_id' : self.next_jenjang_id.id
                        })
                        total_biaya += harga
                else:
                    harga = by.harga
                    
                    if by.is_different_by_gender:
                        if siswa.siswa_id.jenis_kelamin == 'perempuan':
                            harga = by.harga_alt

                    self.env['siswa_keu_ocb11.siswa_biaya'].create({
                        'name' : by.biaya_id.name,
                        'siswa_id' : siswa.siswa_id.id,
                        'tahunajaran_id' : self.next_tahunajaran_id.id,
                        'biaya_id' : by.biaya_id.id,
                        'harga' : harga,
                        'amount_due' : harga,
                        'jenjang_id' : self.next_jenjang_id.id
                    })
                    total_biaya += harga
                        
            # set total_biaya dan amount_due
            res_partner_siswa = self.env['res.partner'].search([('id','=',siswa.siswa_id.id)])
            self.env['res.partner'].search([('id','=',siswa.siswa_id.id)]).write({
                'total_biaya' : res_partner_siswa.total_biaya + total_biaya,
                'amount_due_biaya' : res_partner_siswa.amount_due_biaya + total_biaya,
            }) 

            # compute dashboard keuangan
            self.compute_dashboard_keuangan()

            # set state to done
            self.state = 'done'

    def compute_dashboard_keuangan(self):
        dash_keuangan_id = self.env['ir.model.data'].search([('name','=','default_dashboard_pembayaran')]).res_id
        dash_keuangan = self.env['siswa_keu_ocb11.keuangan_dashboard'].search([('id','=',dash_keuangan_id)])
        for dash in dash_keuangan:
            dash.compute_keuangan()

    def reset_compute_siswa(self):
        self.ensure_one()
        print('-------------------------------')
        print('Resetting Kenaikan Kelas')
        print('-------------------------------')
        if self.state == 'done':
            # rombel_in_jenjangs = self.env['siswa_ocb11.rombel'].search([
            #     ('jenjang_id', '=', self.next_jenjang_id.id)
            # ])
            
            # rombel_ids = []
            # for rombel in rombel_in_jenjangs:
            #     rombel_ids.append(rombel.id)
            
            # # deleting rombel_siswa
            # self.env['siswa_ocb11.rombel_siswa'].search([
            #         ('tahunajaran_id','=', self.next_tahunajaran_id.id),
            #         ('rombel_id','in', rombel_ids),
            #     ]).unlink()

            # reset data rombel siswa dulu
            for siswa in self.siswa_ids:
                # deleting siswa_biaya
                print('Deleting siswa_biaya of ' + siswa.siswa_id.name  )
                self.env['siswa_keu_ocb11.siswa_biaya'].search([
                    ('siswa_id', '=',  siswa.siswa_id.id),
                    ('tahunajaran_id', '=', self.next_tahunajaran_id.id),
                    ('state', '=', 'open'),
                ]).unlink()

                # deleting rombel_siswa
                print('Deleting rombel_siswa of ' + siswa.siswa_id.name  )
                self.env['siswa_ocb11.rombel_siswa'].search([
                    ('tahunajaran_id','=', self.next_tahunajaran_id.id),
                    ('siswa_id','=', siswa.siswa_id.id),
                ]).unlink()
            
            # compute dashboard keuangan
            self.compute_dashboard_keuangan()
            
        else:
            self.siswa_ids.unlink()
            self.is_collected = False
        
        # update state 
        self.state = 'draft'

    def compute_get_siswa(self):
        self.ensure_one()
        rombel_in_jenjangs = self.env['siswa_ocb11.rombel'].search([
            ('jenjang_id', '=', self.jenjang_id.id)
        ])
        rombel_ids = []
        for rombel in rombel_in_jenjangs:
            rombel_ids.append(rombel.id)

        rombel_siswa = self.env['siswa_ocb11.rombel_siswa'].search([
            ('tahunajaran_id', '=', self.tahunajaran_id.id),
            ('rombel_id', 'in', rombel_ids),
        ])

        for rbs in rombel_siswa:
             self.write({
                'siswa_ids' : [(0,0,{
                    'siswa_id' : rbs.siswa_id.id,
                    'jenjang_id' : self.jenjang_id.id,
                    'next_jenjang_id' : self.next_jenjang_id.id,
                    'rombel_id' : rbs.rombel_id.id,
                })]
            })
        
        self.is_collected = True

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

     