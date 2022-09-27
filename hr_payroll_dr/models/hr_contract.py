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
                    ('check_in', '<=', payslip.date_to),
                    ('employee_id', '=', payslip.employee_id.id)
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
                    ('check_in', '<=', payslip.date_to),
                    ('employee_id', '=', payslip.employee_id.id)
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
                    ('check_in', '<=', payslip.date_to),
                    ('employee_id', '=', payslip.employee_id.id)
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
                    ('check_in', '<=', payslip.date_to),
                    ('employee_id', '=', payslip.employee_id.id)
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

    # SALARIO ISR
    def isr_salary(self, payslip):
        result = self.hr_rule_tss_salary(payslip)
        return result

    # Impuesto Sobre la Renta
    def ret_isr(self, payslip, aged_salary, salary_range, tributes):
        result = 0
        salary = self.hr_rule_basic(payslip)
        # aged_salary = self.hr_rule_basic(payslip) * 12

        # salary_range = [
        #     [0, 416220.00, 0],
        #     [416220.01, 624329.00, 0.15],
        #     [624329.01, 867123.00, 0.20],
        #     [867123.01, 0, 0.25]
        # ]

        # tributes = [31216.00, 79776.00]

        if aged_salary >= salary_range[0][0] and aged_salary <= salary_range[0][1]:
            result = 0
        elif aged_salary >= salary_range[1][0] and aged_salary <= salary_range[1][1]:
            result = salary_range[1][2] * salary

        elif aged_salary >= salary_range[2][0] and aged_salary <= salary_range[2][1]:
            result = salary_range[2][2] * salary + tributes[0]

        elif aged_salary >= salary_range[3][0]:
            result = salary_range[3][2] * salary + tributes[1]

        return result

    def cont_infotep(self):
        result = 0
        return result
