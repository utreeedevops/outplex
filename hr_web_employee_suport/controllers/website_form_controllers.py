# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route
from odoo import http
from datetime import datetime


class GeneralRequestRegister(Controller):

    # Este  método llama del backend los datos que se presentan en el formulario de registro.
    @route('/general_request_register', type='http', auth='user', website=True)
    def employees_request_website(self, redirect=None, **post):

        # Devolvemos como respuesta a la petición de page el template del formulario web
        response = request.render("hr_web_employee_suport.employee_request_list_template", {})
        response.headers['X-Frame-Options'] = 'DENY'

        return response


class AbsencesRegister(Controller):

    @route('/absences_register_form', type='http', auth='user', website=True, csrf=False)
    def absences_register_form_redirect(self, redirect=None, **post):

        # Devolvemos como respuesta a la petición de page el template del formulario web
        response = request.render("hr_web_employee_suport.absences_register_template", {})
        response.headers['X-Frame-Options'] = 'DENY'

        return response

    @http.route('/absences_register', type='http', auth='user', website=True)
    def _absences_register(self, **kw):
        print(kw)

        employee_id = request.env['hr.employee'].sudo().search([('pin', '=', kw['e_pin'])])

        request.env['employee.request'].sudo().create({
            'employee_code': kw['e_pin'],
            'employee_id': employee_id.id,
            'notes': kw['description'],
            'request_date': datetime.today(),
        })

        # Llamamos al template creado en XML que nos muestra que el registro fue guardado exitosamente
        return request.render("hr_web_employee_suport.request_saved_template", {})


class AssistanceRequest(Controller):

    @route('/assistance_request_form', type='http', auth='user', website=True, csrf=False)
    def assistance_request_form_redirect(self, redirect=None, **post):

        # Devolvemos como respuesta a la peticion de page el template del formulario web
        response = request.render("hr_web_employee_suport.assistance_request_template", {})
        response.headers['X-Frame-Options'] = 'DENY'

        return response

    @http.route('/assistance_request', type='http', auth='user', website=True)
    def _assistance_request(self, **kw):

        # Llamamos al template creado en XML que nos muestra que el registro fue guardado exitosamente
        return request.render("hr_web_employee_suport.request_saved_template", {})


class GeneralRequests(Controller):

    @route('/general_request_register_form', type='http', auth='user', website=True, csrf=False)
    def general_requests_form_redirect(self, redirect=None, **post):

        # Devolvemos como respuesta a la peticion de page el template del formulario web
        response = request.render("hr_web_employee_suport.general_request_register_template", {})
        response.headers['X-Frame-Options'] = 'DENY'

        return response

    @http.route('/general_request', type='http', auth='user', website=True)
    def _general_requests_register(self, **kw):

        print(kw)

        employee_id = request.env['hr.employee'].sudo().search([('pin', '=', kw['e_pin'])])

        request.env['employee.request'].sudo().create({
            'employee_code': kw['e_pin'],
            'employee_id': employee_id.id,
            'notes': kw['request'],
            'request_date': datetime.today(),
        })

        # Llamamos al template creado en XML que nos muestra que el registro fue guardado exitosamente
        return request.render("hr_web_employee_suport.request_saved_template", {})


class HrPaymentRequest(Controller):

    @route('/payment_request_form', type='http', auth='user', website=True, csrf=False)
    def hr_payment_request_form_redirect(self, redirect=None, **post):

        # Devolvemos como respuesta a la peticion de page el template del formulario web
        response = request.render("hr_web_employee_suport.payment_request_template", {})
        response.headers['X-Frame-Options'] = 'DENY'

        return response

    @http.route('/payment_receipt_request', type='http', auth='user', website=True)
    def _hr_payment_request(self, **kw):

        employee_id = request.env['hr.employee'].sudo().search([('pin', '=', kw['e_pin'])])

        payslip_object = request.env['hr.payslip'].sudo().search([('employee_id', '=', employee_id.id)], limit=1)

        template_id = payslip_object.env.ref('hr_web_employee_suport.web_template_payslip_mail_send')
        template_id.send_mail(payslip_object.id, force_send=True)

        # Llamamos al template creado en XML que nos muestra que el registro fue guardado exitosamente
        return request.render("hr_web_employee_suport.request_saved_template", {})
