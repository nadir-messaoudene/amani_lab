# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class medical_physician(models.Model):
    _name = "medical.physician"
    _description = 'medical physician'
    _rec_name = 'partner_id'

    title = fields.Selection([('dr', 'Dr'), ('Pr', 'Pr'), ('mr', 'Mr'), ('mme', 'Mme')], string=_('Title'))
    partner_id = fields.Many2one('res.partner', _('Physician'), required=True)
    institution_partner_id = fields.Many2one('res.partner', domain=[('is_institution', '=', True)],
                                             string='Institution')
    code = fields.Char('Id')
    info = fields.Text('Extra Info')
