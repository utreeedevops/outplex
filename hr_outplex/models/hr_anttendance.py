from odoo import api, fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    hour_type = fields.Selection(selection=[
        ('regular', 'Regular'),
        ('paid_break', 'DR-Paid Break'),
        ('downtime', 'Downtime'),
        ('refresher', 'Refresher'),
        ('coaching', 'Coaching'),
        ('vacation', 'Vacations'),
        ('support', 'Support'),
        ('training', 'Training'),
        ('day_off', 'Day Off Time')],
        string='Type',
        default='regular'
    )
