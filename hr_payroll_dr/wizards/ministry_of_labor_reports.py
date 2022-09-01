# -*- coding: utf-8 -*-
from odoo import fields, models
from datetime import datetime
import xlsxwriter
import string
import base64


class DGTReports(models.TransientModel):
    _name = 'dgt.reports'
    _description = 'Reportes Y Formularios Para el Ministerio de Trabajo'

    company_id = fields.Many2one('res.company', string=u"Compañía", default=lambda self: self.env.user.company_id)

    date_from = fields.Date("Desde", required=1)
    date_to = fields.Date("Hasta", required=1)

    template = fields.Selection([('dgt34', 'DGT3-DGT4'),
                                 ('tss', 'TSS')],
                                string="Plantilla",
                                required=1,
                                help="Reporte a extraer")

    ministry_of_labour_report_xlsx_file_name = fields.Char()
    ministry_of_labour_report_xlsx_binary = fields.Binary(string="Reporte de Ministerio de Trabajo - XLS")

    def get_xlsx_report(self):

        if self.template == 'dgt34':
            return self.generate_dgt34_report()
        pass

    def generate_dgt34_report(self):
        this = self[0]

        records = []

        contracts = self.env['hr.contract'].search(
                                                    ['|',
                                                     '&',
                                                     ('state', '=', 'open'),
                                                     '&',
                                                     ('date_start', '>=', self.date_from),
                                                     ('date_start', '<=', self.date_to),
                                                     '&',
                                                     ('date_end', '>=', self.date_from),
                                                     '&',
                                                     ('date_end', '<=', self.date_to),
                                                     ('state', '=', 'cancel')])

        employee_list = []

        for rec in contracts:
            if rec.employee_id not in employee_list:
                employee_list.append(rec.employee_id.id)

            # Validations
            birthday = rec.employee_id.birthday

            # if birthday:
            #     birthday = datetime.strptime(birthday, '%Y-%m-%d')

            # Validations: salario

            if rec.schedule_pay == 'hourly':
                salary = (rec.wage * 8) * 23.83

            else:
                salary = rec.wage

            # Validations: type of genre
            employee_gender = rec.employee_id.gender
            gender = ''

            if employee_gender == '':
                pass

            elif employee_gender == 'male':
                gender = 'M'

            elif employee_gender == 'female':
                gender = 'F'

            elif employee_gender == 'other':
                gender = 'O'

            # Validations: type of document
            employee_document = rec.employee_id.identification_id

            document_type = ''

            if employee_document:
                document_type = 'C'

            employee_passport = rec.employee_id.passport_id

            if employee_passport:
                document_type = 'P'

            # Validations: type of nov
            employee_startdate = rec.date_start

            if employee_startdate:
                typenov = 'INGRESO'

            employee_date_end = rec.date_end

            if employee_date_end:
                typenov = 'SALIDA'

            records.append([
                typenov or '',  # Tipo Nov.
                document_type or '',  # Tipo de documento del empleado
                rec.employee_id.identification_id or '',  # Cedula del empleado
                rec.employee_id.name,  # Nombres del empleado
                rec.employee_id.first_lastname,  # 1re. Apellido del empleado
                rec.employee_id.second_lastname,  # 2do. Apellido del empleado
                gender or '',  # Sexo
                rec.employee_id.country_id.name or '',  # Nacionalidad del empleado
                birthday or '',  # Fecha de nacimiento
                salary or 0.0,  # Salario del empleado
                rec.date_start or '',  # Fecha de ingreso
                rec.date_end or '',  # Fecha de salida
                rec.employee_id.job_id.name or '',  # Ocupacion
                rec.employee_id.job_id.description or '',  # Descripcion de la ocupacion
                '',  # Inicio Vacaciones
                '',  # Fin Vacaciones
                '',  # ID Turno
                '',  # ID Establecimiento
                '',  # Fecha Cambio
                '',  # Nivel educativo
                '',  # Discapacidad
            ])

        file_header = [
            u'Tipo Nov.',
            'Tipo Doc.',
            'Número Doc.',
            'Nombres',
            '1re. Apellido',
            '2do. Apellido',
            'Sexo',
            'Nacionalidad',
            'Fecha Nacimiento',
            'Salario',
            'Fecha Ingreso',
            'Fecha Salida',
            'Ocupación',
            'Desc. Ocupación',
            'Inicio Vacaciones',
            'Fin Vacaciones',
            'ID Turno',
            'ID Establecimiento',
            'Fecha Cambio',
            'Nivel educativo',
            'Discapacidad'
        ]

        mfl_date = "{0}{1}{2}".format(self.date_to.year, self.date_to.month, self.date_to.day)

        file_path = '/tmp/REPORTE-{}-{}.xlsx'.format(self.template.upper(), mfl_date)

        workbook = xlsxwriter.Workbook(file_path,
                                       {'strings_to_numbers': True})

        worksheet = workbook.add_worksheet()
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': 1})

        # List the alphabet
        alphabet = ["%s%d" % (l, 1) for l in string.ascii_uppercase]

        for letter, header in zip(alphabet, file_header):
            worksheet.write(str(letter), str(header), bold)

        row = 1
        for rec in records:
            for col, detail in enumerate(rec):
                worksheet.write(row, col, detail)
            row += 1

        workbook.close()

        this.write({
            'ministry_of_labour_report_xlsx_file_name': file_path.replace('/tmp/', ''),
            'ministry_of_labour_report_xlsx_binary': base64.b64encode(
                open(file_path, 'rb').read())
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dgt.reports',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
