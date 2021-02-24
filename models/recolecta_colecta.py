# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

logger = logging.getLogger(__name__)


class recolectacolecta(models.Model):
    _name = 'recolecta.colecta'
    _description = 'Collection book'

    name = fields.Char('Description', required=True)
    date_delivery = fields.Date('Delivery date')
    Deliver_ids = fields.Many2many('res.partner', string='Delivers')
    category_id = fields.Many2one('recolecta.colecta.category', string='Category')

    state = fields.Selection([
        ('draft', 'Unchecked'),
        ('checked', 'checked'),
        ('Lend', 'Lend'),
        ('Cancelled', 'Cancelled')],
        'State', default="draft")

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'checked'),
                   ('checked', 'Lend'),
                   ('Lend', 'checked'),
                   ('checked', 'Cancelled'),
                   ('Lend', 'Cancelled'),
                   ('Cancelled', 'checked')]
        return (old_state, new_state) in allowed

    def change_state(self, new_state):
        for colecta in self:
            if colecta.is_allowed_transition(colecta.state, new_state):
                colecta.state = new_state
            else:
                message = _('Moving from %s to %s is not allowd') % (colecta.state, new_state)
                raise UserError(message)

    def make_checked(self):
        self.change_state('checked')

    def make_Lend(self):
        self.change_state('Lend')

    def make_Cancelled(self):
        self.change_state('Cancelled')

    def log_all_recolecta_members(self):
        recolecta_member_model = self.env['recolecta.member']  # This is an empty recordset of model recolecta.member
        all_members = recolecta_member_model.search([])
        print("ALL MEMBERS:", all_members)
        return True


    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'description': 'Description for parent category',
            'child_ids': [
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        # Total 3 records (1 parent and 2 child) will be craeted in recolecta.colecta.category model
        record = self.env['recolecta.colecta.category'].create(parent_category_val)
        return True

    def change_release_date(self):
        self.ensure_one()
        self.date_delivery = fields.Date.today()

    def find_colecta(self):
        domain = [
            '|',
                '&', ('name', 'ilike', 'colecta Name'),
                     ('category_id.name', '=', 'Category Name'),
                '&', ('name', 'ilike', 'colecta Name 2'),
                     ('category_id.name', '=', 'Category Name 2')
        ]
        colectas = self.search(domain)
        logger.info('colectas found: %s', colectas)
        return True

class recolectaMember(models.Model):

    _name = 'recolecta.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Collection member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    Delivered_colecta_ids = fields.Many2many(
        'recolecta.colecta',
        string='Delivered collections',
        # relation='recolecta_colecta_res_partner_rel'  # optional
    )