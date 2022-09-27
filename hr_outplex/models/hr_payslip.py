from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    referral_bonus = fields.Boolean(string='Has Referrals')
    n_referrals = fields.Integer(string='N. Referral')
