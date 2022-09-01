# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    first_lastname = fields.Char(string='1er. Apellido')
    second_lastname = fields.Char(string='2do. Apellido')
