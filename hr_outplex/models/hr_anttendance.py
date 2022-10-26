# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    # Campo para hacer la identificación de los Diferentes tipos de Horas
    hour_type = fields.Selection(selection=[
        ('regular', 'Regular'),
        ('paid_break', 'DR-Paid Break'),
        ('downtime', 'Downtime'),
        ('refresher', 'Refresher'),
        ('coaching', 'Coaching'),
        ('support', 'Support'),
        ('training', 'Training'),
        ('day_off', 'Day Off Time')],
        string='Type',
        default='regular'
    )

    over_timed = fields.Boolean(string='Over Time', store=True)
