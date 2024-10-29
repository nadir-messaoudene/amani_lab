# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import date, datetime


# classes under  menu of laboratry

class medical_lab(models.Model):
    _name = 'medical.lab'
    _description = 'Medical Lab'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Id")
    test_id = fields.Many2one('medical.test_type', _("Type de prélèvements"), required=True)
    date_analysis = fields.Datetime(_("Date de l'Analysis"), default=datetime.now())
    patient_id = fields.Many2one('medical.patient', _('Patient'), required=True)
    date_requested = fields.Datetime(_('Date de reception'), default=datetime.now())
    medical_lab_physician_id = fields.Many2one('medical.physician', _('Pathologist'))
    requestor_physician_id = fields.Many2one('medical.physician', _('Pathologist'), required=True)
    critearea_ids = fields.One2many('medical_test.critearea', 'medical_lab_id', _('Critaire'))
    results = fields.Text(_('Résultats'))
    notice = fields.Text(_('Avis'))
    diagnosis = fields.Text(_('Diagnostique'))
    is_invoiced = fields.Boolean(copy=False, default=False)
    n_p = fields.Integer("N.P")
    nbr_puddlers = fields.Integer("Nombre de flaquants")
    nbr_blocks = fields.Integer("Nombre de blocs")
    nbr_antibody = fields.Integer("Nombre d'anticorps")
    institution_partner_id = fields.Many2one('res.partner', domain=[('is_clique_laboratory', '=', True)],
                                             string='Clinique/laboratoir', required=True)

    courier_id = fields.Many2one('res.partner', domain=[('is_courier', '=', True)],
                                             string='Coursier', required=True)

    date_macroscopy = fields.Datetime(_('Date de la macroscopie'), default=datetime.now())
    date_technic = fields.Datetime(_('Date de la technique'), default=datetime.now())
    date_lecture = fields.Datetime(_('Date de la lecture'), default=datetime.now())
    IHC = fields.Boolean(_("IHC ?"), default=False)
    sent = fields.Boolean(_("Envoyé ?"), default=False)
    validation = fields.Boolean(_("validation ?"), default=False)

    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('validation', 'Validation'),
        ('email', 'mail envoyé'),
        ('blocked', 'bloque recupéré'),
    ],compute='_compute_validation', default='draft')
    tag_ids = fields.Many2many(
        'crm.tag', 'crm_tag_rel', 'lead_id', 'tag_id', string='Tags',
        help="Classify and analyze your lead/opportunity categories like: Training, Service")
    @api.onchange('status')
    def _compute_validation(self):
        if self.status == 'validation':
            self.validation = True

    @api.model_create_multi
    def create(self, vals_list):
        result = super(medical_lab, self).create(vals_list)
        for val in vals_list:
            val['name'] = self.env['ir.sequence'].next_by_code('ltest_seq')
            if val.get('test_id'):
                critearea_obj = self.env['medical_test.critearea']
                criterea_ids = critearea_obj.search([('test_id', '=', val['test_id'])])
                for id in criterea_ids:
                    critearea_obj.write({'medical_lab_id': result})

        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
