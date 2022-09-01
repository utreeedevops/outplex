from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.contract'

    # Here we are trying to figure out how to calculate all rules  values calculation

    # Salario Básico (Pago Mensual, Quincenal y por Horas)
    def hr_rule_basic(self, payslip):
        result = 0
        for rec in self:
            if rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'monthly':
                result = rec.wage
            elif rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'bi-weekly':
                result = rec.wage/2
            elif rec.wage_type == 'hourly':
                # print('in')
                worked_hours = sum(self.env['hr.attendance'].search([
                    ('check_in', '>=', payslip.date_from),
                    ('check_in', '<=', payslip.date_to)
                ]).mapped('worked_hours'))

                result = worked_hours*rec.hourly_wage

            # print(payslip.date_to)
            # print(payslip.date_from)
        return result

    # SALARIO COTIZABLE TSS
    def hr_rule_tss_salary(self, payslip):
        result = 0
        for rec in self:
            result = rec.hr_rule_basic(payslip)

        return result

    # Descuento Seguro Medico
    def hr_rule_medical_insurance_discount(self):
        return 4783.59 * 0.3

    def hr_rule_taxable(self):
        result = 0
        return result

    def hr_rule_net(self):
        result = 0
        return result

    # SFS Afiliado
    def ret_sfs(self, payslip, sfs_e_percent):
        result = 0
        for rec in self:
            result = 162625 * sfs_e_percent if rec.wage > 162625 else rec.wage * sfs_e_percent
            if rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'monthly':
                result = result

            elif rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'bi-weekly':
                result = result / 2

            elif rec.wage_type == 'hourly':
                # print('in')
                worked_hours = sum(self.env['hr.attendance'].search([
                    ('check_in', '>=', payslip.date_from),
                    ('check_in', '<=', payslip.date_to)
                ]).mapped('worked_hours'))

                amount = rec.hourly_wage * worked_hours

                result = 162625 * sfs_e_percent if amount > 162625 else amount * sfs_e_percent

        return result

    # AFP Afiliado
    def hr_rule_ret_afp(self, payslip, afp_e_percent):
        result = 0
        for rec in self:
            result = 325250 * afp_e_percent if rec.wage > 325250 else rec.wage * afp_e_percent
            if rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'monthly':
                result = result

            elif rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'bi-weekly':
                result = result/2

            elif rec.wage_type == 'hourly':
                # print('in')
                worked_hours = sum(self.env['hr.attendance'].search([
                    ('check_in', '>=', payslip.date_from),
                    ('check_in', '<=', payslip.date_to)
                ]).mapped('worked_hours'))

                amount = rec.hourly_wage * worked_hours

                result = 325250 * afp_e_percent if amount > 325250 else amount * afp_e_percent

        return result

    # SFS Empleador
    def hr_rule_cont_sfs(self, payslip, sfs_percent):
        result = 0
        for rec in self:
            result = 162625 * sfs_percent if rec.wage > 162625 else rec.wage * sfs_percent
            if rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'monthly':
                result = result

            elif rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'bi-weekly':
                result = result / 2

            elif rec.wage_type == 'hourly':
                # print('in')
                worked_hours = sum(self.env['hr.attendance'].search([
                    ('check_in', '>=', payslip.date_from),
                    ('check_in', '<=', payslip.date_to)
                ]).mapped('worked_hours'))

                amount = rec.hourly_wage * worked_hours

                result = 162625 * sfs_percent if amount > 162625 else amount * sfs_percent

        return result

    # AFP Empleador
    def hr_rule_cont_afp(self, payslip, afp_percent):
        result = 0
        for rec in self:
            result = 325250 * afp_percent if rec.wage > 325250 else rec.wage * afp_percent
            if rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'monthly':
                result = result

            elif rec.wage_type == 'monthly' and payslip.struct_id.schedule_pay == 'bi-weekly':
                result = result / 2

            elif rec.wage_type == 'hourly':
                # print('in')
                worked_hours = sum(self.env['hr.attendance'].search([
                    ('check_in', '>=', payslip.date_from),
                    ('check_in', '<=', payslip.date_to)
                ]).mapped('worked_hours'))

                amount = rec.hourly_wage * worked_hours

                result = 325250 * afp_percent if amount > 325250 else amount * afp_percent

        return result

    # Contribución Seguro de Riesgos Laborales (SRL)
    def cont_srl(self):
        result = 0
        for rec in self:
            result = 65050 * (1.3/100) if rec.wage > 65050 else rec.wage * (1.3/100)
        return result

    def ret_isr(self):
        result = 0
        return result

    def cont_infotep(self):
        result = 0
        return result
