# -*- coding: utf-8 -*-
from odoo import api, fields, models
import pytz
from datetime import datetime as dt
import datetime


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    # Agregamos la documentación de las funciones agregadas en las reglas, con la finalidad de que estas puedan ser
    # correctamente usadas en la creación de otras reglas
    amount_python_compute = fields.Text(string='Python Code',
                                        default='''
                        # Available variables:
                        #----------------------
                        # payslip: object containing the payslips
                        # employee: hr.employee object
                        # contract: hr.contract object
                        # -------------------------Doc---------------------------------
                        #   Tipo de Horas
                        #   'regular' - Regular
                        #   'paid_break' - DR-Paid Break
                        #   'downtime' - Downtime
                        #   'refresher' - Refresher
                        #   'coaching' - Coaching
                        #   'support' - Support
                        #   'training' - Training
                        #   'day_off' - Day Off Time
                        #
                        #   contract.worked_hour_total(payslip, hour_types)
                        #
                        # rules: object containing the rules code (previously computed)
                        # categories: object containing the computed salary rule categories (sum of amount of all rules belonging to that category).
                        # worked_days: object containing the computed worked days.
                        # inputs: object containing the computed inputs.
                        # 

                        # Note: returned value have to be set in the variable 'result'

                        result = contract.wage * 0.10''')


class HrContract(models.Model):
    _inherit = 'hr.contract'

    bonus_rate = fields.Monetary(string='Bonus Rate')
    hiring_referral_bonus = fields.Monetary(string='Referral Bonus')

    training_rate = fields.Monetary(string='Training Rate')
    transportation_bonus = fields.Monetary(string='Transportation Bonus Wage')

    def worked_hour_total(self, payslip, hour_types):
        hour_types_total = 0
        for rec in self:
            hour_types_total = sum(self.env['hr.attendance'].search([
                ('hour_type', 'in', hour_types),
                ('check_in', '>=', payslip.date_from),
                ('check_in', '<=', payslip.date_to),
                ('employee_id', '=', payslip.employee_id)]).mapped('worked_hours'))

            # hour_types_total -= self.hours_after_nine(payslip=payslip)

        return hour_types_total

    def hours_after_nine(self, payslip, hour_types=None, ranges=None):
        if ranges is None:
            ranges = [21, 8]

        if hour_types is None:
            hour_types = ['day_off']

        hours_after_nine = 0
        for rec in self:
            attendances_after_nine = self.env['hr.attendance'].search([
                ('hour_type', 'not in', hour_types),
                ('check_in', '>=', payslip.date_from),
                ('check_in', '<=', payslip.date_to),
                ('employee_id', '=', payslip.employee_id)]).filtered(lambda a: ranges[0] <= (a.check_in.hour - datetime.timedelta(hours=5)))

            for attendance in attendances_after_nine:
                hours_after_nine += (attendance.check_out - attendance.check_in).seconds / 3600

                print('after nine', hours_after_nine)

        return hours_after_nine
