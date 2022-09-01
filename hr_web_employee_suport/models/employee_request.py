# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EmployeeRequest(models.Model):
    _name = 'employee.request'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    employee_code = fields.Char(string='Employee Code')

    request_date = fields.Date(string='Request Date')

    notes = fields.Html(string='Description')

    status = fields.Selection([('attend', 'Atendido'),
                               ('un_attend', 'No Atendido'),
                               ('cancel', 'Cancelado')], default='un_attend')
