# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    referral_bonus = fields.Boolean(string='Has Referrals')
    n_referrals = fields.Integer(string='N. Referral')

    add_in_bonus = fields.Monetary(string='Add In Bonus')

    add_vacations = fields.Boolean(string='Has Vacation')
    vacation_days = fields.Float(string='Vacation Days')
    hours_per_day = fields.Float(string='Hours Per Day')
